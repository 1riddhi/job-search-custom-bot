import json

def load_seen():
    try:
        return set(json.load(open("jobs.json")))
    except:
        return set()

def save_seen(data):
    json.dump(list(data), open("jobs.json", "w"))