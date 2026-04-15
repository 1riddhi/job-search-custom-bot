import time
from fetchers.amazon import fetch_amazon
from fetchers.greenhouse import fetch_greenhouse
from fetchers.postman import fetch_postman
from utils.discord import send
from utils.storage import load_seen, save_seen
from config import GREENHOUSE_COMPANIES

def main():
    print("🚀 CLEAN JOB BOT\n")

    all_jobs = []

    all_jobs += fetch_amazon()

    for company, board in GREENHOUSE_COMPANIES:
        all_jobs += fetch_greenhouse(company, board)

    all_jobs += fetch_postman()

    print("📊 Jobs:", len(all_jobs))

    seen = load_seen()
    new_seen = set(seen)

    for job in all_jobs:
        uid = f"{job['company']}_{job['id']}"

        if uid in seen:
            continue

        send(job)
        new_seen.add(uid)
        time.sleep(0.2)

    save_seen(new_seen)

if __name__ == "__main__":
    main()