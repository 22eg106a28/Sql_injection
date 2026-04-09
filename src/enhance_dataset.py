import pandas as pd
import random
import re

# ----------------------------
# Load Existing Dataset
# ----------------------------
df = pd.read_csv("https://raw.githubusercontent.com/ankitkumarhello20/sql-injection-dataset/main/SqlQueriesData.csv")

# Adjust column names if needed
df.columns = [col.lower() for col in df.columns]

# Assuming:
# query column = 'query'
# label column = 'label'

# ----------------------------
# Feature Extraction
# ----------------------------
def extract_features(query):
    q = str(query).lower()

    return {
        "query_length": len(q),
        "num_quotes": q.count("'") + q.count('"'),
        "count_equals": q.count("="),
        "count_parentheses": q.count("(") + q.count(")"),

        "has_union": int("union" in q),
        "has_select": int("select" in q),
        "has_drop": int("drop" in q),
        "has_insert": int("insert" in q),
        "has_delete": int("delete" in q),
        "has_update": int("update" in q),

        "has_or_1_equals_1": int("or 1=1" in q),
        "has_comment": int("--" in q or "#" in q),
        "has_sleep": int("sleep" in q),
        "has_semicolon": int(";" in q),
    }

# ----------------------------
# Generate Extra Data
# ----------------------------
def generate_normal(n=300):
    queries = []
    for _ in range(n):
        q = f"SELECT * FROM users WHERE id={random.randint(1,1000)}"
        queries.append((q, 0))
    return queries

def generate_injection(n=300):
    queries = []
    for _ in range(n):
        q_type = random.choice(["or", "union", "drop", "sleep"])

        if q_type == "or":
            q = f"' OR {random.randint(1,100)}={random.randint(1,100)} --"
        elif q_type == "union":
            q = "SELECT * FROM users WHERE id=1 UNION SELECT password FROM users"
        elif q_type == "drop":
            q = "SELECT * FROM users; DROP TABLE users;"
        else:
            q = f"' OR SLEEP({random.randint(1,5)}) --"

        queries.append((q, 1))
    return queries

# ----------------------------
# Combine Data
# ----------------------------
new_data = generate_normal(300) + generate_injection(300)

df_new = pd.DataFrame(new_data, columns=["query", "label"])

# Merge with original dataset
df_combined = pd.concat([df, df_new], ignore_index=True)

# ----------------------------
# Feature Engineering
# ----------------------------
feature_df = df_combined["query"].apply(lambda x: pd.Series(extract_features(x)))

df_final = pd.concat([df_combined, feature_df], axis=1)

# Shuffle dataset
df_final = df_final.sample(frac=1).reset_index(drop=True)

# Save
df_final.to_csv("final_sql_dataset.csv", index=False)

print("✅ Final dataset created: final_sql_dataset.csv")
print("Shape:", df_final.shape)