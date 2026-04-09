import joblib
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load once
model = load_model("sql_model.h5")
tokenizer = joblib.load("tokenizer.pkl")
scaler = joblib.load("scaler.pkl")
selected_features = joblib.load("features.pkl")


def extract_features(query):
    return {
        'digits': sum(c.isdigit() for c in query),
        'spl_char': sum(not c.isalnum() for c in query),
        'query_length': len(query),
        'num_quotes': query.count("'") + query.count('"'),
        'count_equals': query.count('='),
        'count_parentheses': query.count('(') + query.count(')'),
        'operator': int(any(op in query.lower() for op in [' or ', ' and '])),
        'has_union': int('union' in query.lower()),
        'has_select': int('select' in query.lower()),
        'has_comment': int('--' in query or '/*' in query),
        'safekywrd': int('where' in query.lower())
    }


def predict_query(query):

    seq = tokenizer.texts_to_sequences([query])
    pad = pad_sequences(seq, maxlen=100)

    feat = extract_features(query)
    feat_df = pd.DataFrame([feat])[selected_features]
    feat_scaled = scaler.transform(feat_df)

    prob = model.predict([pad, feat_scaled])[0][0]

    label = "Injection" if prob > 0.5 else "Safe"

    return label, float(prob)