import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Personal Finance Analytics",
    page_icon="💰",
    layout="wide"
)


# -----------------------------
# Load data
# -----------------------------

@st.cache_data
def load_data():
    csv_path = "data/expenses.csv"

    data = pd.read_csv(csv_path)
    data["date"] = pd.to_datetime(data["date"])

    return data


@st.cache_data
def load_budget():
    return pd.read_csv("data/budget.csv")


data = load_data()
budget = load_budget()


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🔎 Filters")

categories = ["All"] + sorted(
    data["category"].unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

payment_methods = ["All"] + sorted(
    data["payment_method"].unique().tolist()
)

selected_payment = st.sidebar.selectbox(
    "Payment Method",
    payment_methods
)


# -----------------------------
# Apply filters
# -----------------------------

filtered_data = data.copy()

if selected_category != "All":
    filtered_data = filtered_data[
        filtered_data["category"] == selected_category
    ]

if selected_payment != "All":
    filtered_data = filtered_data[
        filtered_data["payment_method"] == selected_payment
    ]


# -----------------------------
# Title
# -----------------------------

st.title("💰 Personal Finance Analytics")

st.caption(
    "Interactive spending, budget and financial behavior analysis"
)


# -----------------------------
# Metrics
# -----------------------------

total_spending = filtered_data["amount"].sum()

average_transaction = (
    filtered_data["amount"].mean()
    if not filtered_data.empty
    else 0
)

transaction_count = len(filtered_data)

if not filtered_data.empty:

    highest_category = (
        filtered_data
        .groupby("category")["amount"]
        .sum()
        .idxmax()
    )

else:

    highest_category = "N/A"


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Spending",
        f"₹{total_spending:,.0f}"
    )


with col2:

    st.metric(
        "Average Transaction",
        f"₹{average_transaction:,.0f}"
    )


with col3:

    st.metric(
        "Transactions",
        transaction_count
    )


with col4:

    st.metric(
        "Top Category",
        highest_category
    )


st.divider()


# -----------------------------
# Spending by Category
# -----------------------------

st.subheader("📊 Spending by Category")

category_spending = (
    filtered_data
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)


if not category_spending.empty:

    st.bar_chart(category_spending)

else:

    st.warning(
        "No transactions match the selected filters."
    )


# -----------------------------
# Monthly Spending
# -----------------------------

st.subheader("📈 Monthly Spending")


if not filtered_data.empty:

    monthly_spending = (
        filtered_data
        .set_index("date")
        .resample("ME")["amount"]
        .sum()
    )

    monthly_spending.index = (
        monthly_spending.index
        .strftime("%Y-%m")
    )

    st.line_chart(monthly_spending)

else:

    st.info("No monthly data available.")


# -----------------------------
# Budget Analysis
# -----------------------------

st.subheader("💵 Budget Analysis")


if not category_spending.empty:

    budget_lookup = budget.set_index("category")["budget"]

    budget_analysis = category_spending.to_frame(
        "Spent"
    )

    budget_analysis["Budget"] = (
        budget_analysis.index.map(budget_lookup)
    )

    budget_analysis["Budget"] = (
        budget_analysis["Budget"].fillna(0)
    )

    budget_analysis["Remaining"] = (
        budget_analysis["Budget"]
        - budget_analysis["Spent"]
    )

    budget_analysis["Status"] = (
        budget_analysis["Remaining"]
        .apply(
            lambda x:
            "✅ Within Budget"
            if x >= 0
            else "⚠️ Over Budget"
        )
    )

    st.dataframe(
        budget_analysis,
        width="stretch"
    )


# -----------------------------
# Spending Insights
# -----------------------------

st.subheader("💡 Spending Insights")


if not filtered_data.empty:

    highest_transaction = filtered_data.loc[
        filtered_data["amount"].idxmax()
    ]

    st.write(
        f"💳 **Largest transaction:** "
        f"₹{highest_transaction['amount']:,.0f} "
        f"({highest_transaction['category']} - "
        f"{highest_transaction['description']})"
    )

    if not category_spending.empty:

        top_category = category_spending.idxmax()

        top_amount = category_spending.max()

        st.write(
            f"📌 **Highest spending category:** "
            f"{top_category} "
            f"(₹{top_amount:,.0f})"
        )

    st.write(
        f"📊 **Average transaction value:** "
        f"₹{average_transaction:,.0f}"
    )

else:

    st.info("No insights available.")


# -----------------------------
# Transactions
# -----------------------------

st.subheader("🧾 Transactions")

st.dataframe(
    filtered_data.sort_values(
        "date",
        ascending=False
    ),
    width="stretch"
)


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "Personal Finance Analytics | "
    "Python • Pandas • SQLite • Scikit-learn • Streamlit"
)