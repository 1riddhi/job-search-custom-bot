import time
import argparse
import os
import hashlib
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from fetchers.amazon import fetch_amazon
from fetchers.greenhouse import fetch_greenhouse
from fetchers.postman import fetch_postman
from fetchers.microsoft import fetch_microsoft
from fetchers.uber import fetch_uber
from utils.discord import send
from utils.storage import load_seen, save_seen
from config import GREENHOUSE_COMPANIES


def make_uid(job):
    """
    Safe unique ID across all sources (Microsoft, Greenhouse, etc.)
    """
    raw = (
        job.get("company", "") +
        job.get("title", job.get("name", "")) +
        str(job.get("id", job.get("atsJobId", job.get("displayJobId", "")))) +
        str(job.get("link", job.get("url", job.get("positionUrl", ""))))
    )
    return hashlib.md5(raw.encode()).hexdigest()


def run_once():
    print(f"\n🚀 Job Alert Automation — run at {datetime.now().isoformat(timespec='seconds')}\n")

    all_jobs = []

    # Fetch all sources
    all_jobs += fetch_uber()
    # all_jobs += fetch_amazon()
    # all_jobs += fetch_microsoft()

    for company, board in GREENHOUSE_COMPANIES:
        all_jobs += fetch_greenhouse(company, board)

    all_jobs += fetch_postman()

    print("📊 Jobs fetched:", len(all_jobs))

    seen = load_seen()
    new_seen = set(seen)

    sent_count = 0

    for job in all_jobs:
        uid = make_uid(job)

        if uid in seen:
            continue

        try:
            send(job)
            sent_count += 1
            new_seen.add(uid)
            time.sleep(0.2)

        except Exception as e:
            print("[DISCORD ERROR]", e)

    save_seen(new_seen)

    print(f"📨 Sent to Discord: {sent_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one time and exit (default runs on schedule).",
    )
    args = parser.parse_args()

    if args.once:
        run_once()
        raise SystemExit(0)

    cron_expr = (os.environ.get("JOB_CRON") or "0 */6 * * *").strip()
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

    # Run immediately once on startup
    run_once()

    print(f"⏱️ Scheduler started (JOB_CRON='{cron_expr}'). Press Ctrl+C to stop.")
    scheduler.start()