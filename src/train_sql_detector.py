from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Replace with better dataset later
texts = [
    "SELECT * FROM users",
    "INSERT INTO table VALUES (1, 'abc')",
    "DELETE FROM users WHERE id=1",
    "DROP TABLE students",
    "hello how are you",
    "this is normal text",
    "machine learning is fun",
    "what is your name"
]

labels = [1, 1, 1, 1, 0, 0, 0, 0]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

joblib.dump(model, "sql_detector.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("SQL detector trained and saved!")