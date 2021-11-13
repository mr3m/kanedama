from datetime import date
from joblib import dump, load
from typing import List

import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, validator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

PERIODS = [f'{day}d' for day in (1, 5, 7, 10, 14, 30, 45, 50, 60)]


class Account(BaseModel):
    update_date: date
    balance: float


class Transaction(BaseModel):
    amount: float
    date: date


class RequestTrain(BaseModel):
    accounts: List[Account]
    transactions: List[List[Transaction]]


class RequestPredict(BaseModel):
    account: Account
    transactions: List[Transaction]

    @validator("transactions")
    def validate_transaction_history(cls, v, *, values):
        # validate that
        # - the transaction list passed has at least 6 months history
        # - no transaction is posterior to the account's update date
        if len(v) < 1:
            raise ValueError("Must have at least one transaction")

        update_t = values["account"].update_date

        oldest_t = v[0].date
        newest_t = v[0].date
        for t in v[1:]:
            if t.date < oldest_t:
                oldest_t = t.date
            if t.date > newest_t:
                newest_t = t.date

        assert (
            update_t - newest_t
        ).days >= 0, "Update Date Inconsistent With Transaction Dates"
        assert (update_t - oldest_t).days > 183, "Not Enough Transaction History"

        return v


class ResponsePredict(BaseModel):
    predicted_amount: float


class TransactionTimeSeries:
  '''Encapsulates a single transaction time series'''

  def __init__(self, transactions: pd.DataFrame, balance: Account):
    self.transactions = transactions
    self.balance = balance
    self.transaction_date_start = self.transactions.index.min()
    self.transaction_date_last = self.transactions.index.max()
    self.transaction_date_span = self.transaction_date_last - self.transaction_date_start

  def incoming_transactions(self):
    '''Returns the transactions with a positive amount'''
    return TransactionTimeSeries(self.transactions[self.transactions > 0].dropna(), self.balance)

  def outgoing_transactions(self):
    '''Returns the transactions with a negative amount'''
    return TransactionTimeSeries(self.transactions[self.transactions < 0].dropna(), self.balance)

  def transactions_after_n_days(self, number_of_days: int):
    '''Returns the transactions spanning from the start date up until the start date plus the given number of days'''
    return TransactionTimeSeries(
      self.transactions.loc[self.transaction_date_start:self.transaction_date_start + pd.DateOffset(number_of_days), :],
      self.balance)

  def transactions_from_n_to_m_days(self, n_number_of_days: int, m_number_of_days: int):
    '''Returns the transactions spanning from the start date + n days up until the start date + m days'''
    return TransactionTimeSeries(
      self.transactions.loc[
      self.transaction_date_start + pd.DateOffset(
        n_number_of_days):self.transaction_date_start + pd.DateOffset(
        m_number_of_days), :],
      self.balance)

  def resample(self, frequency: str) -> pd.DataFrame:
    '''Returns a timeseries resampled by a given frequency'''
    return self.transactions.resample(frequency)

  def __call__(self) -> pd.DataFrame:
    return self.transactions


def transaction_to_timeseries(single_transactions: List[Transaction], account: List[Account]) -> TransactionTimeSeries:
    single_transactions_df = pd.DataFrame(map(dict, single_transactions))
    single_transactions_df['date'] = pd.to_datetime(single_transactions_df.date)
    single_transactions_df = single_transactions_df.set_index('date')
    return TransactionTimeSeries(single_transactions_df, account)


def preprocess_data(transactions: List[List[Transaction]], accounts: List[Account]) -> List[TransactionTimeSeries]:
    timeseries_list = []
    for single_transactions, account in zip(transactions, accounts):
        transaction_timeseries = transaction_to_timeseries(single_transactions, account)
        if transaction_timeseries.transaction_date_span.days > 180:
            timeseries_list.append(transaction_timeseries)

    return timeseries_list


def compute_timeseries_features(timeseries, number_of_days):
    return (
        timeseries.transactions_after_n_days(number_of_days).incoming_transactions()().sum().amount,
        # The sum of incoming transactions
        timeseries.transactions_after_n_days(number_of_days).outgoing_transactions()().sum().amount,
        # The sum of outgoing transactions
        timeseries.transactions_after_n_days(number_of_days)().sum().amount,
        # This should be a proxy of the balance,
        # that is the sum of outgoing and incoming transactions up to the cut date `n`
        timeseries.transactions_after_n_days(number_of_days)().cumsum().mean().amount,
        # The mean balance
        *[timeseries.transactions_after_n_days(number_of_days).incoming_transactions(
        ).resample('d').sum().rolling(period).sum().dropna().mean().amount
        for period in PERIODS],
        # The rolling mean of incoming transactions at various periods
        *[timeseries.transactions_after_n_days(number_of_days).outgoing_transactions(
        ).resample('d').sum().rolling(period).sum().dropna().mean().amount
        for period in PERIODS],
        # The rolling mean of outgoing transactions at various periods
        timeseries.transactions_from_n_to_m_days(
        number_of_days, number_of_days + 30).outgoing_transactions()().sum().amount
        # The sum of outgoing transactions on the 30 days after the cut date `n`, that is the label to predict
    )


def build_training_set(timeseries_list: List[TransactionTimeSeries], number_of_days: int):
    return pd.DataFrame(
        [compute_timeseries_features(timeseries, number_of_days)
        for timeseries in timeseries_list
        ],
        columns=[
        'incoming_sum',
        'outgoing_sum',
        'estimated_balance',
        'mean_balance',
        *[f'income_{period}_rolling_mean' for period in PERIODS],
        *[f'outcome_{period}_rolling_mean' for period in PERIODS],
        'outgoing_to_predict'
        ]
    ).dropna()


def construct_training_set(dataset, target_label='outgoing_to_predict'):
    '''Make a training and testing set'''
    training_sets = dict()
    (
        training_sets['X_train'],
        training_sets['X_test'],
        training_sets['y_train'],
        training_sets['y_test']
    ) = train_test_split(
        dataset.drop(target_label, axis=1).to_numpy(),
        dataset[target_label].to_numpy(),
        test_size=0.2, random_state=0)
    return training_sets


def train(transactions: List[List[Transaction]], accounts: List[Account]) -> dict:
    transaction_training_set = construct_training_set(
        build_training_set(
        preprocess_data(transactions, accounts), 150)
    )
    estimator = RandomForestRegressor().fit(transaction_training_set['X_train'], transaction_training_set['y_train'])
    dump(estimator, 'estimator.joblib')
    return {
        'score': estimator.score(transaction_training_set['X_test'], transaction_training_set['y_test'])
    }


def predict(transactions: List[Transaction], account: Account) -> float:
    estimator = load('estimator.joblib')
    transaction_timeseries = transaction_to_timeseries(transactions, account)
    prediction_timeseries = pd.DataFrame(build_training_set([transaction_timeseries],
                                    transaction_timeseries.transaction_date_span.days
                                    )).drop('outgoing_to_predict', axis=1)
    prediction_timeseries['estimated_balance'] = account.balance # Use actual balance
    prediction = estimator.predict(
        prediction_timeseries.to_numpy()
    )[0]
    return prediction


app = FastAPI()


@app.post("/train")
async def train_root(train_body: RequestTrain):
    training_state = train(train_body.transactions, train_body.accounts)
    return {"training": training_state}


@app.post("/predict")
async def predict_root(predict_body: RequestPredict):

    transactions = predict_body.transactions
    account = predict_body.account

    predicted_amount = predict(transactions, account)

    # Return predicted amount
    return {"predicted_amount": predicted_amount}
