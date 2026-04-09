import joblib

# Load trained model + vectorizer
sql_model = joblib.load("sql_detector.pkl")
vectorizer = joblib.load("vectorizer.pkl")

SQL_KEYWORDS = [
    "select", "insert", "update", "delete",
    "drop", "union", "where", "from", "join",
    "create", "alter", "truncate",
    "group by", "order by", "having",
    "limit", "offset", "values"
]

def is_sql_like(text):
    text = text.lower()
    return any(keyword in text for keyword in SQL_KEYWORDS)

def is_sql_query_ml(text):
    X = vectorizer.transform([text])
    pred = sql_model.predict(X)[0]
    return pred == 1

def is_sql_query(text):
    # Hybrid approach
    if not is_sql_like(text):
        return False
    
    return is_sql_query_ml(text)