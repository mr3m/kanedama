import json
from datetime import date

import requests


# You can use this function to test your api
# Make sure the uvicorn server is running locally on `http://127.0.0.1:8000/`
# or change the hardcoded localhost below
def get_test_accounts():
    test_accounts = [
        {"balance": 10*n, "update_date": str(date(2020, 11, 3))}
        for n in range(1, 10)
    ]
    return test_accounts


def get_test_transactions():
    test_transactions = [
        {"date": str(date(2020, i, j)), "amount": -100}
        for i in range(1, 10)
        for j in [5, 17, 26]
    ]
    return test_transactions


def test_train():
    """
    Test the training route with test date
    """
    test_data = {
        "accounts": get_test_accounts(),
        "transactions": get_test_transactions(),
    }

    print("Calling train route on API with test data:")
    print(test_data)

    response = requests.post(
        "http://127.0.0.1:8000/train", data=json.dumps(test_data)
    )

    print("Response: ")
    print(response.json())

    assert response.status_code == 200


def test_predict():
    """
    Test the predict route with test data
    """
    test_data = {
        "account": get_test_accounts()[0],
        "transactions": get_test_transactions(),
    }

    print("Calling predict route on API with test data:")
    print(test_data)

    response = requests.post(
        "http://127.0.0.1:8000/predict", data=json.dumps(test_data)
    )

    print("Response: ")
    print(response.json())

    assert response.status_code == 200


if __name__ == "__main__":
    test_train()
    test_predict()
