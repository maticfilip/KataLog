import requests
import json
import os
import re

OLLAMA_URL="http://localhost:11434"
SETTINGS_FILE="data/llm_settings.json"
DEFAULT_MODEL="phi3:mini"

VALID_CATEGORIES = [
    "Algorithms", "Data Structures", "String Manipulation",
    "Mathematics", "Language Features", "Other"
]

def get_selected_model():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_MODEL
    with open(SETTINGS_FILE, "r") as f:
        content=f.read().strip()
        if not content:
            return DEFAULT_MODEL
        data=json.loads(content)
        return data.get("model", DEFAULT_MODEL)
    
def set_selected_model(model):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"model":model}, f, indent=2)

def is_ollama_running():
    try:
        response=requests.get(OLLAMA_URL, timeout=2)
        return response.status_code==200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False

def get_available_models():
    try:
        response=requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        data=response.json()
        return [m["name"] for m in data.get("models", [])]
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return []
    
def generate(prompt:str, on_complete, on_error=None):
    import threading

    def worker():
        try:
            model=get_selected_model()
            response=requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model":model, "prompt":prompt, "stream":False},
                timeout=120
            )
            response.raise_for_status()
            text=response.json().get("response","")
            on_complete(text)
        except Exception as e:
            if on_error:
                on_error(str(e))
        
    threading.Thread(target=worker, daemon=True).start()




def parse_json_response(raw:str):
    match=re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        return {"topic":"Unknown", "category":"Other", "explanation":raw}
    try:
        data=json.loads(match.group())
        valid_categories=[
            "Algorithms","Data Structures","String Manipulation","Mathematics","Language Features","Other"
        ]
        if data.get("category") not in valid_categories:
            data["category"]="Other"
        return data
    except json.JSONDecodeError:
        return {"topic":"Unknown","category":"Other","explanation":raw}


def explain_topic(kata_name, difficulty, description, code, on_complete, on_error=None):
    prompt = f"""You are a coding mentor. A student just completed this Codewars kata:

    Kata: {kata_name} ({difficulty})
    Description: {description}
    Their solution:
    {code}

    Do two things:
    1. Explain the key theoretical concept behind this kata in 2-3 paragraphs, suitable for a beginner-intermediate developer.
    2. Categorize it.

    Respond ONLY in this exact JSON format, with no other text before or after:
    {{
    "topic": "short topic name, 2-4 words",
    "category": "one of: Algorithms, Data Structures, String Manipulation, Mathematics, Language Features, Other",
    "explanation": "your full explanation here"
    }}"""

    def handle_raw(raw: str):
        on_complete(parse_json_response(raw))

    generate(prompt, on_complete=handle_raw, on_error=on_error)

def get_code_feedback(kata_name, difficulty, code, on_complete, on_error=None):
    prompt=f"""You are a coding mentor reviewing a CodeWars solution.
    Kata: {kata_name} ({difficulty})

Solution:
{code}

Give brief, constructive feedback covering:
1. Code readability
2. Efficiency or edge cases missed
3. One alternative approach if applicable

Keep it concise and encouraging. Write 2-3 short paragraphs, no headers or bullet points."""

    generate(prompt, on_complete=on_complete, on_error=on_error)

def generate_weekly_review(entries,on_complete,on_error=None):
    if not entries:
        on_complete("No kata logged this week, nothing to review yet.")
        return
    summary_lines=[]
    for e in entries:
        line=f"-{e["kata_name"]}({e["difficulty"]}, {e.get("language","unknown")})-{e["status"]}"
        if e.get("notes"):
            line+=f". Notes: {e["notes"]}"
        summary_lines.append(line)
    week_summary="\n".join(summary_lines)

    prompt = f"""You are a coding mentor reviewing a student's week of Codewars practice.

This week's kata:
{week_summary}

Write a short, encouraging weekly review covering:
1. What they practiced and any patterns you notice
2. Any difficulty or topic they seemed to struggle with
3. One concrete suggestion for next week

Keep it warm and concise, 3-4 short paragraphs, no headers or bullet points."""

    generate(prompt, on_complete=on_complete, on_error=on_error)
