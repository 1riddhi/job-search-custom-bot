import requests
from config import HEADERS
from filters import is_role, is_india, extract_yoe

def fetch_amazon():
    try:
        r = requests.get(
            "https://www.amazon.jobs/en/search.json?base_query=software+engineer",
            headers=HEADERS,
            timeout=10
        ).json()
    except:
        return []

    jobs = []

    for j in r.get("jobs", []):
        if is_role(j.get("title")) and is_india(j.get("location")):
            jobs.append({
                "id": j["id"],
                "title": j["title"],
                "company": "Amazon",
                "location": j.get("location"),
                "link": "https://www.amazon.jobs" + j.get("job_path", ""),
                "yoe": extract_yoe(j.get("description", ""))
            })

    return jobs