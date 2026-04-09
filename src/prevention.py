def prevention_tips(query):

    query_lower = query.lower()
    tips = []

    if "'" in query or '"' in query:
        tips.append("Use parameterized queries (prepared statements).")

    if "union" in query_lower:
        tips.append("Restrict UNION queries and validate inputs.")

    if "--" in query or "/*" in query:
        tips.append("Block SQL comment patterns in input.")

    if " or " in query_lower or " and " in query_lower:
        tips.append("Sanitize logical operators (OR/AND).")

    if "drop" in query_lower or "delete" in query_lower:
        tips.append("Restrict destructive SQL commands.")

    if not tips:
        tips.append("Apply input validation and least privilege principle.")

    return tips


import re

def sanitize_query(query):

    q = query.lower()

    # 1. Remove SQL comments
    q = re.sub(r'--.*', '', q)
    q = re.sub(r'/\*.*?\*/', '', q)

    # 2. Remove dangerous patterns
    patterns = [
        r"or\s+1=1",
        r"and\s+1=1",
        r"or\s+'1'='1'",
        r"union\s+select",
        r"drop\s+table",
        r"delete\s+from",
        r"insert\s+into",
        r"update\s+\w+",
        r"exec\s+",
    ]

    for p in patterns:
        q = re.sub(p, '', q)

    # 3. Remove extra quotes
    q = q.replace("'", "")
    q = q.replace('"', "")

    # 4. Remove multiple spaces
    q = re.sub(r'\s+', ' ', q).strip()

    return q