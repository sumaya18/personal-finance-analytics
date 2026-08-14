# 💰 Personal Finance Analytics

An end-to-end personal finance analytics application built with Python, SQLite, Pandas, Scikit-learn, and Streamlit.

The project analyzes spending behavior, detects unusual transactions using machine learning, predicts future spending, evaluates model performance, and provides an interactive dashboard for managing transactions.

---

## 🚀 Features

### 📊 Spending Analytics
- Total spending calculation
- Average transaction value
- Category-wise spending analysis
- Monthly spending trends
- Payment-method analysis
- Budget tracking

### 🚨 Anomaly Detection
Uses **Isolation Forest** to identify unusual transactions based on:
- Transaction amount
- Spending category
- Payment method

### 🔮 Spending Prediction
Uses **Linear Regression** to estimate next month's spending based on historical monthly spending.

### 🧪 Model Evaluation
The prediction model is evaluated using:
- Mean Absolute Error (MAE)
- R² Score
- Actual vs. predicted spending comparison

### 🗄️ SQLite Database
Transactions are stored in a relational SQLite database instead of relying only on CSV files.

### ✏️ Transaction Management
Users can:
- Add expenses
- Edit transactions
- Delete transactions
- Filter transactions

### 🧪 Automated Testing
The project includes **pytest** tests covering:
- Database availability
- Database schema
- Data validation
- Monthly aggregation
- ML prediction
- Prediction error calculation

---

## 🏗️ Project Architecture

```text
personal-finance-analytics/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── expenses.csv
│   ├── budget.csv
│   └── finance.db
│
├── notebooks/
│
├── src/
│   ├── main.py
│   ├── database.py
│   ├── generate_data.py
│   ├── anomaly_detection.py
│   ├── spending_prediction.py
│   └── model_evaluation.py
│
├── tests/
│   └── test_finance.py
│
├── README.md
└── requirements.txt