import requests
import json
import os
from datetime import date, datetime

PROFILE_FILE="core\data\cw_profile.json"
COMPLETED_FILE="data/cw_completed.json"
BASE_URL="https://www.codewars.com/api/v1"

def save(path, data):
    os.makedirs("data",exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        content=f.read().strip()
        if not content:
            return None
        return json.loads(content)

def fetch_profile(username):
    url=f"{BASE_URL}/users/{username}"
    response=requests.get(url)

    if response.status_code==404:
        return {"error":"User not found"}
    if response.status_code!=200:
        return {"error":f"API error: {response.status_code}"}
    
    data=response.json()
    save(PROFILE_FILE, data)
    return data

def fetch_completed(username):
    all_kata=[]
    page=0

    while True:
        url=f"{BASE_URL}/users/{username}/code-challenges/completed?page={page}"
        response=requests.get(url)

        if response.status_code!=200:
            break

        data=response.json()
        all_kata.extend(data.get("data",[]))

        if page>=data.get("totalPages", 1)-1:
            break

        page+=1

    save(COMPLETED_FILE, all_kata)
    return all_kata

def fetch_all(username):
    profile=fetch_profile(username)
    if "error" in profile:
        return profile
    fetch_completed(username)
    return profile

def load_profile():
    return load(PROFILE_FILE)

def load_completed():
    return load(COMPLETED_FILE) or []

def get_completed_this_month():
    completed=load_completed()
    today=date.today()
    return sum(
        1 for k in completed
        if datetime.fromisoformat(
            k["completedAt"].replace("Z","+00:00")
        ).month==today.month
        and datetime.fromisoformat(
            k["completedAt"].replace("Z", "+00:00")
        ).year==today.year
    )

def get_language_breakdown():
    completed=load_completed()
    counts={}
    for kata in completed:
        for lang in kata.get("completedLanguages", []):
            counts[lang]=counts.get(lang,0)+1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def get_language_ranks():
    profile=load_profile()
    if not profile:
        return {}
    return profile.get("ranks", {}).get("languages",{})

    
def get_username():
    profile=load_profile()
    if profile:
        return profile.get("username")
    return None

def disconnect():
    for path in [PROFILE_FILE, COMPLETED_FILE]:
        if os.path.exists(path):
            os.remove(path)

if __name__=="__main__":
    data=fetch_profile("maticfilip")
    print(data)