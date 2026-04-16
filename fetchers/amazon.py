import requests
from config import HEADERS
from filters import is_role, is_india, extract_yoe

AMAZON_URL = (
    "https://www.amazon.jobs/en/search.json"
    "?base_query=software+engineer"
    "&loc_query=India"
    "&country=IND"
    "&result_limit=50"
)


def fetch_amazon():
    print("\n🔵 Amazon fetch started")

    try:
        resp = requests.get(AMAZON_URL, headers=HEADERS, timeout=10)

        print("[Amazon STATUS]", resp.status_code)

        if resp.status_code != 200:
            print("[Amazon ERROR] Bad status")
            return []

        if "json" not in (resp.headers.get("Content-Type") or ""):
            print("[Amazon BLOCKED / HTML RESPONSE]")
            return []

        data = resp.json()

    except Exception as e:
        print("[Amazon ERROR]", e)
        return []

    jobs = data.get("jobs", [])
    print("[Amazon] jobs found:", len(jobs))

    result = []

    for j in jobs:
        title = j.get("title", "") or ""
        location = j.get("location", "") or ""
        desc = j.get("description", "") or ""

        # 🔥 SAFE SKIPS
        if not title:
            continue

        if not is_role(title):
            continue

        if not is_india(location):
            continue

        # 🔥 FIXED YOE (IMPORTANT FIX)
        yoe = extract_yoe(title + " " + desc)

        result.append({
            "id": j.get("id", title),
            "title": title,
            "company": "Amazon",
            "location": location,
            "link": "https://www.amazon.jobs" + (j.get("job_path") or ""),
            "yoe": yoe
        })

    print("[Amazon FINAL JOBS]", len(result))
    return result