import requests
from filters import is_role, is_india, extract_yoe

UBER_URL = "https://www.uber.com/api/loadSearchJobs?location=India"


def fetch_uber():
    print("\n🟣 Uber fetch started")

    try:
        resp = requests.get(UBER_URL, timeout=10)
        print("[Uber STATUS]", resp.status_code)

        if "json" not in (resp.headers.get("Content-Type") or ""):
            print("[Uber BLOCKED or HTML]")
            return []

        data = resp.json()

    except Exception as e:
        print("[Uber ERROR]", e)
        return []

    jobs = data.get("data", {}).get("jobs", [])

    result = []

    for j in jobs:
        title = j.get("title", "")
        location = j.get("location", "")

        if not is_role(title):
            continue

        if not is_india(location):
            continue

        result.append({
            "id": j.get("id", title),
            "title": title,
            "company": "Uber",
            "location": location,
            "link": j.get("applyUrl") or "",
            "yoe": extract_yoe(j.get("description", ""))
        })

    print("[Uber FINAL JOBS]", len(result))
    return result