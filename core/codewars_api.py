import requests
import json
import os

PROFILE_FILE="data/cw_profile.json"
BASE_URL="https://www.codewars.com/api/v1"

def fetch_profile(username):
    url=f"{BASE_URL}/users/{username}"
    response=requests.get(url)

    if response.status_code==404:
        return {"error":"User not found"}
    if response.status_code!=200:
        return {"error":f"API error: {response.status_code}"}
    
    data=response.json()
    os.makedirs("data",exist_ok=True)
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return data

def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return None
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)
    
def get_username():
    profile=load_profile()
    if profile:
        return profile.get("username")
    return None

if __name__=="__main__":
    data=fetch_profile("maticfilip")
    print(data)