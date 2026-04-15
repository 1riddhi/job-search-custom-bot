import time
import argparse
from datetime import datetime
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from fetchers.amazon import fetch_amazon
from fetchers.greenhouse import fetch_greenhouse
from fetchers.postman import fetch_postman
from utils.discord import send
from utils.storage import load_seen, save_seen
from config import GREENHOUSE_COMPANIES

def run_once():
    print(f"🚀 CLEAN JOB BOT — run at {datetime.now().isoformat(timespec='seconds')}\n")

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one time and exit (default runs every 2 minutes).",
    )
    args = parser.parse_args()

    if args.once:
        run_once()
        raise SystemExit(0)

    cron_expr = (os.environ.get("JOB_CRON") or "*/2 * * * *").strip()
    trigger = CronTrigger.from_crontab(cron_expr)

    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_once,
        trigger,
        id="job-bot",
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
    )

    # Run immediately on startup, then on schedule.
    run_once()
    print(f"⏱️  Scheduler started (JOB_CRON='{cron_expr}'). Press Ctrl+C to stop.")
    scheduler.start()