import json
import os
from datetime import datetime

THEORY_FILE = "data/theory.json"

CATEGORIES = [
    "Algorithms",
    "Data Science",
    "Machine Learning",
    "Data Structures",
    "String Manipulation",
    "Mathematics",
    "Regex",
    "Language Features",
    "Other"
]

def load():
    if not os.path.exists(THEORY_FILE):
        return []
    with open(THEORY_FILE, "r") as f:
        content=f.read().strip()
        if not content:
            return []
        return json.loads(content)

# def save(entries):
#     os.makedirs("data", e)