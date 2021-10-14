<p align="center"><a href="https://github.com/MansaGroup/kanedama" target="blank"><img src="../.github/assets/logo.png" width="80" alt="Mansa's Logo" /></a></p>
<h1 align="center">Mansa's Kanedama</h1>
<p align="center">Take home test to <b>join us</b> 💜</p>

# The Mission

Your mission, should you choose to accept it, is to demonstrate your ability to deal with time-series data, build a model, and serve it using an API framework. Your task is to use the provided data  (more info at the bottom) to design a model capable of making predictions.

Your model should then be served through the small [FastAPI](https://fastapi.tiangolo.com/) file provided. 

## Before you pick a model

You will deal with bank account transactions data. We suggest you take a look and explore them. Since those are real data, they are noisy and sparse, and there may be duplicated data. Some columns such as dates might need to be parsed as such.

Build a function to check which accounts have more than 180 days of history - you can discard the others for your models and analysis.

_You can assume that any account passed to your service will have at least 6 months of history._

## Predict next month outgoing given the past 6 months of transactions

Set up a prediction function that takes a list of accounts, a list of transactions and a user, and ouputs a prediction for the aggregated next month outgoing for that user.

Outgoing is defined as the sum of all transactions with `< 0` amount over a certain time-period. So to get the monthly outgoing, you can sum the transactions over monthly periods.

> **Tip.** It might make more sense to define a month as a 30 day period rather than the month itself since the snapshots can be taken at any point during the month and not necessarily at the end. 

> **Tip 2.** By combining the transactions and accounts data you should be able to reverse the balance of the account back through time (back to the oldest transaction date for the account). This information might be useful as a feature of your predicting model.

# Delivery

To achieve your mission, you'll have to deliver:

- A documented `Python` (3.x) code with a `readme.md`.
- An API serving your prediction model based on `FastAPI`.
- Notebooks and/or plots to support your decision process.

Your solution must be able to run and respond to requests (it can take as long to calculate as you want). You can imagine it as a micro-service that could be run independently on a server.

**What's important for us**

We would like you to motivate your choices and to discuss the strengths and weaknesses of your approach, and possible ways to improve your predictions. 

**What's not (so) important for us**

- You can use whatever other external software libraries you think are appropriate: Pandas/numpy/scikit-learn are encouraged!
- The preprocessing/algorithms/loss functions and the split between train/validation/test set are yours to decide.
- You do not necessarily have to use all the data if you feel like some of it is irrelevant or not useful. 
- We are not going to penalize you for accuracy.

# The Weapons we provide you

In the `data` folder, you will find three `csv` files containing real anonymized data from transactions, accounts and users:

- The `transactions.csv` contains a set of transactions with an amount (in EUR) and the date of the day they were added.
- The `accounts.csv` contains a list of balances for the accounts that the transactions pertain to.
- The `users.csv` contains a list of the account owners with the date of the last update of their financial data. Note that the balance provided for each account is the balance at the update date of the user the account belongs to.

> **Tip 3.** The available transaction history on each account is defined as the time elapsed since the oldest transaction on this account and the **update date** of the account, not the date of the latest transaction on the account. If the date of the latest transaction on the account is older than the update date, that simply means that no transactions were recorded on the account in this time period.

> **Tip 4.** Some users may have several accounts. While the update date is the same for all the different accounts of a given user, the length of the available transaction history is not necessarily the same.

# FastAPI 101

Provided with this repo is also a `main.py` file with a minimal [FastAPI](https://fastapi.tiangolo.com/) demo. Once you have installed the `requirements.txt` in your `Python` environment you will be able to run the main file by simply calling
`uvicorn main:app` inside your directory. This should start the local server and you should be able to see the automatically generated API docs at `http://127.0.0.1:8000/docs`.

In order to serve your model in the API, move your preprocessing to a function which you can call any input on. You do not have to worry about validating the inputs FastAPI will do this for you! You can then move your predict functionality to the `predict` function in `main.py` and return the predicted amount.

You can test your API using the `test_main.py` file, just make sure you are running the server by calling `uvicorn main:app` in another terminal window.

If you use `pandas`, you can convert the `transactions` of type `List[Transaction]` (or similarly the `accounts` of type `List[Account]`) passed to the API to a `pd.DataFrame` by calling:

```python
import pandas as pd

df = pd.DataFrame(map(dict, transactions))
```

This is because the objects passed to the API are using `pydantic`'s `BaseModel` class which allows easy conversion from object to dictionary through the default `.dict()` implementation.

If you wish to learn more about how to use `FastAPI`:

- [Official FastAPI Docs](https://fastapi.tiangolo.com/)
- [Official pydantic Docs](https://pydantic-docs.helpmanual.io/)
- [Medium Post: How to Deploy a Machine Learning Model](https://towardsdatascience.com/how-to-deploy-a-machine-learning-model-dc51200fe8cf)
