import requests
from datetime import datetime
import time
import re

from config import HEADERS, MAX_HOURS
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
        title = j.get("title", "")
        location = j.get("location", {}).get("name", "")

        if not is_role(title):
            continue

        if not is_india(location):
            continue

        # optional time filter
        updated = j.get("updated_at") or j.get("created_at")
        if updated:
            try:
                ts = time.mktime(datetime.strptime(updated[:19], "%Y-%m-%dT%H:%M:%S").timetuple())
                age_hours = (time.time() - ts) / 3600
                if age_hours > MAX_HOURS:
                    continue
            except:
                pass

        jobs.append({
            "id": j["id"],
            "title": title,
            "company": company,
            "location": location,
            "link": j.get("absolute_url"),
            "yoe": extract_yoe(j.get("content", ""))
        })

    return jobs