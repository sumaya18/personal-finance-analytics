import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    return pd.read_csv("data/expenses.csv")


def load_budget():
    return pd.read_csv("data/budget.csv")


def calculate_total_spending(data):
    return data["amount"].sum()


def spending_by_category(data):
    return data.groupby("category")["amount"].sum()


def find_highest_category(category_spending):
    category = category_spending.idxmax()
    amount = category_spending.max()
    return category, amount


def spending_by_month(data):
    data["date"] = pd.to_datetime(data["date"])
    data["month"] = data["date"].dt.to_period("M")

    return data.groupby("month")["amount"].sum()


def analyze_budget(category_spending, budget):
    budget_analysis = category_spending.to_frame("spent")

    budget_analysis["budget"] = (
        budget.set_index("category")["budget"]
    )

    budget_analysis["difference"] = (
        budget_analysis["budget"] - budget_analysis["spent"]
    )

    return budget_analysis


def show_category_chart(category_spending):
    category_spending.plot(kind="bar")

    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.tight_layout()
    plt.show()


def show_monthly_chart(monthly_spending):
    monthly_spending.plot(kind="line", marker="o")

    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.grid()
    plt.tight_layout()
    plt.show()


def show_budget_status(budget_analysis):
    print("\nBudget Status:")

    for category, row in budget_analysis.iterrows():

        if row["difference"] >= 0:
            print(
                f"{category}: Within budget "
                f"(₹{row['difference']:.0f} remaining)"
            )
        else:
            print(
                f"{category}: OVER BUDGET "
                f"(₹{abs(row['difference']):.0f} exceeded)"
            )


def main():

    data = load_data()
    budget = load_budget()

    total = calculate_total_spending(data)

    category_spending = spending_by_category(data)

    highest_category, highest_amount = find_highest_category(
        category_spending
    )

    monthly_spending = spending_by_month(data)

    budget_analysis = analyze_budget(
        category_spending,
        budget
    )

    print("========== PERSONAL FINANCE ANALYTICS ==========")

    print("\nTotal Spending:")
    print(f"₹{total:.2f}")

    print("\nSpending by Category:")
    print(category_spending)

    print("\nHighest Spending Category:")
    print(f"{highest_category} - ₹{highest_amount:.2f}")

    print("\nMonthly Spending:")
    print(monthly_spending)

    print("\nBudget Analysis:")
    print(budget_analysis)

    show_budget_status(budget_analysis)

    show_category_chart(category_spending)

    show_monthly_chart(monthly_spending)


if __name__ == "__main__":
    main()