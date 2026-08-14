import sqlite3
import pandas as pd


DATABASE_PATH = "data/finance.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def import_csv_data():
    data = pd.read_csv("data/expenses.csv")

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("DELETE FROM transactions")

    data.to_sql(
        "transactions",
        connection,
        if_exists="append",
        index=False
    )

    connection.commit()
    connection.close()


def get_transactions():
    connection = sqlite3.connect(DATABASE_PATH)

    data = pd.read_sql_query(
        "SELECT * FROM transactions",
        connection
    )

    connection.close()

    return data


if __name__ == "__main__":
    create_database()
    import_csv_data()

    data = get_transactions()

    print("Database created successfully!")
    print(f"Transactions loaded: {len(data)}")
    print(data.head())
    