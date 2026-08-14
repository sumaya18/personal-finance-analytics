import sqlite3
import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


DATABASE_PATH = "data/finance.db"


def test_database_exists():

    assert Path(DATABASE_PATH).exists()


def test_transactions_table_exists():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='transactions'
        """,
        connection
    )

    connection.close()

    assert len(tables) == 1


def test_transactions_have_required_columns():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    data = pd.read_sql_query(
        "SELECT * FROM transactions",
        connection
    )

    connection.close()

    required_columns = {
        "id",
        "date",
        "category",
        "description",
        "amount",
        "payment_method"
    }

    assert required_columns.issubset(
        set(data.columns)
    )


def test_transaction_amounts_are_positive():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    data = pd.read_sql_query(
        "SELECT amount FROM transactions",
        connection
    )

    connection.close()

    assert (data["amount"] > 0).all()


def test_transaction_dates_are_valid():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    data = pd.read_sql_query(
        "SELECT date FROM transactions",
        connection
    )

    connection.close()

    dates = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    assert dates.notna().all()


def test_monthly_data_generation():

    dates = pd.date_range(
        "2025-01-01",
        "2025-06-30",
        freq="D"
    )

    data = pd.DataFrame(
        {
            "date": dates,
            "amount": np.random.randint(
                100,
                1000,
                len(dates)
            )
        }
    )

    monthly = (
        data
        .set_index("date")
        .resample("ME")["amount"]
        .sum()
    )

    assert len(monthly) == 6


def test_linear_regression_prediction():

    X = np.array(
        [
            [1],
            [2],
            [3],
            [4],
            [5]
        ]
    )

    y = np.array(
        [
            1000,
            1200,
            1400,
            1600,
            1800
        ]
    )

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    prediction = model.predict(
        [[6]]
    )[0]

    assert prediction > 1800


def test_prediction_error():

    actual = np.array(
        [
            1000,
            2000,
            3000
        ]
    )

    predicted = np.array(
        [
            1100,
            1900,
            3100
        ]
    )

    mae = mean_absolute_error(
        actual,
        predicted
    )

    assert mae == 100.0