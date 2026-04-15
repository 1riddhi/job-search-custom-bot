import requests
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send(job):
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not set (env or .env)")

    payload = {
        "embeds": [{
            "title": job["title"],
            "description": (
                f"🏢 {job['company']}\n"
                f"📍 {job['location']}\n"
                f"📊 YOE: {job.get('yoe')}"
            ),
            "url": job["link"],
            "color": 5814783
        }]
    }

    resp = requests.post(WEBHOOK_URL, json=payload, timeout=15)
    if resp.status_code >= 300:
        raise RuntimeError(f"Discord webhook failed: {resp.status_code} {resp.text[:300]}")