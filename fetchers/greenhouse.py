import requests
from config import HEADERS
from filters import is_role, is_india, extract_yoe

def fetch_greenhouse(company, board):
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()
    except:
        return []

    jobs = []

    for j in data.get("jobs", []):
        if is_role(j.get("title")) and is_india(j.get("location", {}).get("name")):
            jobs.append({
                "id": j["id"],
                "title": j["title"],
                "company": company,
                "location": j.get("location", {}).get("name"),
                "link": j.get("absolute_url"),
                "yoe": extract_yoe(j.get("content", ""))
            })

    return jobs