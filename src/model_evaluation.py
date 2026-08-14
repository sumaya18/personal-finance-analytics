import sqlite3
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


DATABASE_PATH = "data/finance.db"


def load_data():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    data = pd.read_sql_query(
        "SELECT date, amount FROM transactions",
        connection
    )

    connection.close()

    data["date"] = pd.to_datetime(
        data["date"]
    )

    return data


def prepare_monthly_data(data):

    monthly = (
        data
        .set_index("date")
        .resample("ME")["amount"]
        .sum()
        .reset_index()
    )

    monthly["month_number"] = np.arange(
        1,
        len(monthly) + 1
    )

    return monthly


def main():

    data = load_data()

    monthly = prepare_monthly_data(
        data
    )

    if len(monthly) < 6:

        print(
            "Not enough monthly data."
        )

        return

    # Use the first 75% for training
    split_index = int(
        len(monthly) * 0.75
    )

    train = monthly.iloc[
        :split_index
    ]

    test = monthly.iloc[
        split_index:
    ]

    X_train = train[
        ["month_number"]
    ]

    y_train = train[
        "amount"
    ]

    X_test = test[
        ["month_number"]
    ]

    y_test = test[
        "amount"
    ]

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    results = test[
        ["date", "amount"]
    ].copy()

    results["predicted"] = predictions

    results["error"] = (
        results["amount"]
        - results["predicted"]
    )

    print(
        "\n======================================"
    )

    print(
        "        MODEL EVALUATION"
    )

    print(
        "======================================"
    )

    print(
        f"\nTraining months: {len(train)}"
    )

    print(
        f"Testing months: {len(test)}"
    )

    print(
        f"\nMAE: ₹{mae:,.2f}"
    )

    print(
        f"R² Score: {r2:.4f}"
    )

    print(
        "\nActual vs Predicted:"
    )

    print(
        results.to_string(
            index=False
        )
    )


if __name__ == "__main__":

    main()