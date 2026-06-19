import requests

OLLAMA_URL="http://localhost:11434"

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