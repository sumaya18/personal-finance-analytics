import sqlite3
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression


DATABASE_PATH = "data/finance.db"


def load_transactions():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    data = pd.read_sql_query(
        """
        SELECT date, amount
        FROM transactions
        """,
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


def train_model(monthly):

    X = monthly[
        ["month_number"]
    ]

    y = monthly[
        "amount"
    ]

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    return model


def predict_next_month(
    model,
    monthly
):

    next_month_number = (
        len(monthly) + 1
    )

    prediction = model.predict(
        [[next_month_number]]
    )[0]

    return max(
        0,
        prediction
    )


def main():

    data = load_transactions()

    if data.empty:

        print(
            "No transactions found."
        )

        return


    monthly = prepare_monthly_data(
        data
    )


    print(
        "\n========== MONTHLY SPENDING =========="
    )

    print(
        monthly[
            [
                "date",
                "amount"
            ]
        ].to_string(
            index=False
        )
    )


    if len(monthly) < 2:

        print(
            "\nNot enough monthly data "
            "to train the model."
        )

        return


    model = train_model(
        monthly
    )


    prediction = predict_next_month(
        model,
        monthly
    )


    last_month = monthly[
        "date"
    ].iloc[-1]


    next_month = (
        last_month
        + pd.DateOffset(
            months=1
        )
    )


    print(
        "\n========== SPENDING PREDICTION =========="
    )

    print(
        f"Predicted spending for "
        f"{next_month.strftime('%Y-%m')}: "
        f"₹{prediction:,.2f}"
    )


if __name__ == "__main__":

    main()