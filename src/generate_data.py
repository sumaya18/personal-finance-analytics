import pandas as pd
import numpy as np
from pathlib import Path


np.random.seed(42)


OUTPUT_FILE = Path("data/expenses.csv")


categories = {
    "Food": [
        "Groceries",
        "Restaurant",
        "Coffee",
        "Snacks"
    ],
    "Transport": [
        "Uber",
        "Bus",
        "Fuel",
        "Auto"
    ],
    "Shopping": [
        "Clothing",
        "Electronics",
        "Online Shopping"
    ],
    "Bills": [
        "Internet",
        "Electricity",
        "Mobile",
        "Water"
    ],
    "Entertainment": [
        "Movie",
        "Games",
        "Subscription"
    ],
    "Health": [
        "Medicine",
        "Pharmacy",
        "Doctor"
    ],
    "Education": [
        "Course",
        "Books",
        "Learning"
    ]
}


payment_methods = [
    "UPI",
    "Card",
    "Cash",
    "Bank Transfer"
]


category_ranges = {
    "Food": (150, 2500),
    "Transport": (80, 1800),
    "Shopping": (500, 7000),
    "Bills": (300, 2500),
    "Entertainment": (200, 2500),
    "Health": (200, 3000),
    "Education": (300, 5000)
}


dates = pd.date_range(
    start="2025-08-01",
    end="2026-07-31",
    freq="D"
)


transactions = []


for date in dates:

    number_of_transactions = np.random.randint(
        0,
        4
    )

    for _ in range(number_of_transactions):

        category = np.random.choice(
            list(categories.keys())
        )

        description = np.random.choice(
            categories[category]
        )

        minimum, maximum = (
            category_ranges[category]
        )

        amount = np.random.randint(
            minimum,
            maximum + 1
        )

        payment_method = np.random.choice(
            payment_methods
        )

        transactions.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "category": category,
                "description": description,
                "amount": amount,
                "payment_method": payment_method
            }
        )


data = pd.DataFrame(
    transactions
)


# Add a small number of unusually large
# transactions for anomaly detection.

anomalies = pd.DataFrame(
    [
        {
            "date": "2026-02-15",
            "category": "Shopping",
            "description": "High Value Purchase",
            "amount": 45000,
            "payment_method": "Card"
        },
        {
            "date": "2026-04-10",
            "category": "Entertainment",
            "description": "Unusual Purchase",
            "amount": 30000,
            "payment_method": "Card"
        },
        {
            "date": "2026-06-20",
            "category": "Shopping",
            "description": "Large Electronics Purchase",
            "amount": 55000,
            "payment_method": "Card"
        }
    ]
)


data = pd.concat(
    [
        data,
        anomalies
    ],
    ignore_index=True
)


data = data.sort_values(
    "date"
)


data.to_csv(
    OUTPUT_FILE,
    index=False
)


print(
    "======================================"
)

print(
    "      DATASET GENERATED SUCCESSFULLY"
)

print(
    "======================================"
)

print(
    f"Transactions: {len(data)}"
)

print(
    f"Start date: {data['date'].min()}"
)

print(
    f"End date: {data['date'].max()}"
)

print(
    f"Total spending: "
    f"₹{data['amount'].sum():,.0f}"
)

print(
    f"Saved to: {OUTPUT_FILE}"
)