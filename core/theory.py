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

def save(entries):
    os.makedirs("data", exist_ok=True)
    with open(THEORY_FILE,"w") as f:
        json.dump(entries, f, indent=2)

def add_topic(topic: str, category: str, explanation: str, related_kata: str = "", related_kata_id: str = "") -> dict:
    entries=load()
    entry={
        "id":datetime.now().strftime("%Y%m%d-%H%M%S"),
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic":topic,
        "category":category if category in CATEGORIES else "Other",
        "explanation":explanation,
        "related_kata":related_kata,
        "related_kata_id":related_kata_id
    }
    entries.append(entry)
    save(entries)
    return entry

def get_topics():
    return list(reversed(load()))

def get_topics_by_category(category):
    return [t for t in get_topics() if t["category"]==category]

def get_category_counts():
    topics=get_topics()
    counts={cat: 0 for cat in CATEGORIES}
    for t in topics:
        cat=t.get("category","Other")
        if cat in counts:
            counts[cat]+=1
    return counts

def delete_topic(topic_id):
    entries=load()
    entries=[e for e in entries if e["id"] != topic_id]
    save(entries)

def search_topics(query):
    query=query.lower()
    return [
        t for t in get_topics()
        if query in t["topic"].lower() or query in t["explanation"].lower()
    ]
