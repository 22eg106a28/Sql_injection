import streamlit as st
import pandas as pd

from src.predict import predict_query
from src.prevention import prevention_tips, sanitize_query
from src.sql_detector import is_sql_query


# =========================
# 🔐 Simple Login System
# =========================
def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid Credentials")


# =========================
# 🚀 Main App
# =========================
def main_app():

    st.title("🔐 SQL Injection Detection System")

    # 🔹 Sample Queries
    sample_queries = [
        "SELECT * FROM users;",
        "SELECT * FROM users WHERE id=10;",
        "' OR 1=1 --",
        "SELECT * FROM users WHERE id=1 UNION SELECT username, password FROM admin;",
        "admin' --",
        "SELECT name FROM employees WHERE salary > 50000"
    ]

    mode = st.radio("Select Mode:", ["Manual Query", "Upload File"])

    # =====================
    # Manual Mode
    # =====================
    if mode == "Manual Query":

        selected_sample = st.selectbox("Try Sample Queries", [""] + sample_queries)
        query = st.text_area("Enter SQL Query", value=selected_sample)

        if st.button("Analyze Query"):

            if query.strip() == "":
                st.warning("Please enter a query.")
                return

            # Step 1: Check if SQL or not
            if not is_sql_query(query):
                 st.warning("⚠️ This is NOT a SQL query.")
                 return

            # Step 2: Run injection detection
            label, prob = predict_query(query)

            if label == "Injection":
                st.error(f"🚨 Injection Detected (Confidence: {prob:.4f})")

                st.subheader("🛡️ Prevention Tips")
                for tip in prevention_tips(query):
                    st.write(f"- {tip}")

                st.subheader("🧼 Sanitized Query")
                sanitized = sanitize_query(query)
                st.code(sanitized)

            else:
                st.success(f"✅ Safe Query (Confidence: {prob:.4f})")

    # =====================
    # File Upload Mode
    # =====================
    else:

        file = st.file_uploader(
            "Upload CSV or SQL file",
            type=["csv", "sql", "txt"]
        )

        if file is not None:

            # Handle CSV
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)

                if 'query' not in df.columns:
                    st.error("CSV must contain 'query' column")
                    return

                queries = df['query'].tolist()

            # Handle SQL / TXT
            else:
                content = file.read().decode("utf-8")

                # Split queries using ;
                queries = [q.strip() for q in content.split(";") if q.strip()]

            results = []

            for q in queries:
                if not is_sql_query(q):
                    results.append({
                        "query": q,
                        "result": "Not SQL",
                        "confidence": 0.0
                    })
                    continue

            label, prob = predict_query(q)

            result_df = pd.DataFrame(results)
            st.dataframe(result_df)


# =========================
# 🔄 Session Control
# =========================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    main_app()