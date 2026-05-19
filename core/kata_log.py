import json
import os
from datetime import datetime, date, timedelta

KATA_FILE="data/kata_log.json"

DIFFICULTIES=["8kyu","7kyu","6kyu","5kyu","4kyu","3kyu","2kyu","1kyu"]
STATUSES=["Solved","Struggled","Gave up","Learning"]

def load():
    if not os.path.exists(KATA_FILE):
        return []
    with open(KATA_FILE, "r") as f:
        content=f.read().strip()
        if not content:
            return []
        return json.loads(content)
    
def save(entries):
    os.makedirs("data",exist_ok=True)
    with open(KATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)

def add_entry(kata_name, difficulty,status,description,notes,code):
    entries=load()
    entries.append({
        "id":datetime.now().strftime("%Y%m%d-%H%M%S"),
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kata_name":kata_name,
        "difficulty":difficulty,
        "status":status,
        "description":description,
        "notes":notes,
        "code":code
    })
    save(entries)

def get_entries():
    return list(reversed(load()))

def search_entries(query):
    query=query.lower()
    return [
        e for e in get_entries()
        if query in e["kata_name"].lower() or query in e["notes"].lower()
    ]

def group_by_day(entries):
    groups={}
    for entry in entries:
        day=entry["timestamp"][:10]
        if day not in groups:
            groups[day]=[]
        groups[day].append(entry)
    return groups

def get_stats():
    entries=load()
    today=str(date.today())
    this_week=[
        e for e in entries
        if (date.today() - date.fromisoformat(e["timestamp"][:10])).days<7
    ]

    return {
        "total":len(entries),
        "this_week":len(this_week),
        "done_today":any(e["timestamp"][:10]==today for e in entries)
    }

def get_streak():
    entries=load()
    today=date.today()
    result=[]
    for i in range(6,-1,-1):
        day=str(today-timedelta(days=i))
        did_kata=any(e["timestamp"][:10]==day for e in entries)
        result.append(did_kata)
    return result

def get_streak_number():
    streak=get_streak()
    count=0
    for did in reversed(streak):
        if did:
            count+=1
        else:
            break
    return count

def calculate_weekly_entries():
    entries=load()
    today = datetime.now()
    count=0
    start_of_week = today.replace(hour=0, minute=0, second=0, microsecond=0) \
                        - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    for entry in entries:
        date=datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if start_of_week <= date <end_of_week:
            count+=1
    return count

def check_today():
    entries=load()
    today=str(date.today())
    return any(e["timestamp"][:10]==today for e in entries)

def delete_entry_by_id(entry_id):
    entries=load()
    entries=[e for e in entries if e["id"] != entry_id]
    save(entries)