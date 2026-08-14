import sqlite3
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


DATABASE_PATH = "data/finance.db"


def load_transactions():
    connection = sqlite3.connect(DATABASE_PATH)

    data = pd.read_sql_query(
        "SELECT * FROM transactions",
        connection
    )

    connection.close()

    return data


def detect_anomalies(data):

    features = [
        "amount",
        "category",
        "payment_method"
    ]

    X = data[features].copy()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "category",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                ["category"]
            ),
            (
                "payment_method",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                ["payment_method"]
            ),
            (
                "amount",
                "passthrough",
                ["amount"]
            )
        ]
    )

    model = IsolationForest(
        n_estimators=200,
        contamination=0.15,
        random_state=42
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X)

    data["anomaly_prediction"] = pipeline.predict(X)

    data["anomaly_status"] = (
        data["anomaly_prediction"]
        .map({
            1: "Normal",
            -1: "Unusual"
        })
    )

    return data


def main():

    data = load_transactions()

    if data.empty:

        print("No transactions found in database.")

        return

    results = detect_anomalies(data)

    unusual_transactions = results[
        results["anomaly_prediction"] == -1
    ]

    print("\n======================================")
    print("       TRANSACTION ANOMALY DETECTION")
    print("======================================")

    print(
        f"\nTotal transactions: {len(results)}"
    )

    print(
        f"Unusual transactions: "
        f"{len(unusual_transactions)}"
    )

    print("\nUnusual Transactions:")

    if unusual_transactions.empty:

        print("No unusual transactions detected.")

    else:

        display_columns = [
            "date",
            "category",
            "description",
            "amount",
            "payment_method",
            "anomaly_status"
        ]

        print(
            unusual_transactions[
                display_columns
            ].to_string(index=False)
        )


if __name__ == "__main__":
    main()