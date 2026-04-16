import requests
from filters import is_role, is_india, extract_yoe

SEARCH_API = "https://apply.careers.microsoft.com/api/pcsx/search"
DETAIL_API = "https://apply.careers.microsoft.com/api/pcsx/position_details"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://careers.microsoft.com/"
}


def get_details(job_id):
    url = f"{DETAIL_API}?position_id={job_id}&domain=microsoft.com&hl=en"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        return None

    try:
        return r.json().get("data", {})
    except:
        return None


def fetch_microsoft(keyword="software engineer"):
    jobs = []

    url = SEARCH_API + "?domain=microsoft.com&query=" + keyword + "&location=India&start=0&sort_by=match&filter_include_remote=1"

    resp = requests.get(url, headers=HEADERS)

    print("\n[Microsoft STATUS]", resp.status_code)

    if "application/json" not in resp.headers.get("content-type", ""):
        print("[Microsoft ERROR] BLOCKED HTML RESPONSE")
        print(resp.text[:200])
        return []

    try:
        data = resp.json()
    except:
        print("[Microsoft ERROR] JSON parse failed")
        return []

    positions = data.get("data", {}).get("positions", [])

    print(f"[Microsoft] keyword={keyword} jobs={len(positions)}")

    for job in positions:
        job_id = job.get("id")
        title = job.get("name", "")
        locations = job.get("locations", [])

        if not is_role(title):
            continue

        if not is_india(locations):
            continue

        detail = get_details(job_id)
        if not detail:
            continue

        desc = detail.get("jobDescription", "")

        yoe = extract_yoe(desc)

        if yoe is None or yoe > 2:
            continue

        jobs.append({
            "id": job_id,
            "title": title,
            "company": "Microsoft",
            "location": locations,
            "yoe": yoe,
            "link": (
                "https://apply.careers.microsoft.com/careers"
                f"?domain=microsoft.com&start=0&location=India"
                f"&pid={job_id}&sort_by=distance&filter_include_remote=1"
            )
        })

    return jobs