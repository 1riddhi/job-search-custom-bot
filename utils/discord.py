import requests
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send(job):
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

    requests.post(WEBHOOK_URL, json=payload)