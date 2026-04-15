# Job Alert Bot

Fetches job listings and posts **new** jobs to a Discord channel via webhook.

## Requirements

- Python 3.9+ recommended

## Setup

Create a virtualenv and install dependencies:

```bash
python -m venv venv
./venv/bin/python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

## Run

Run once (useful for testing):

```bash
./venv/bin/python main.py --once
```

Run continuously using the built-in scheduler:

```bash
./venv/bin/python main.py
```

## Schedule (cron-style)

`main.py` uses APScheduler and reads the schedule from the `JOB_CRON` environment variable (standard **5-field** crontab format).

- **Default**: every 6 hours (unless you change the default in `main.py`)
- **Example: every 2 minutes**

```bash
JOB_CRON="*/2 * * * *" ./venv/bin/python main.py
```

- **Example: every 6 hours (explicit)**

```bash
JOB_CRON="0 */6 * * *" ./venv/bin/python main.py
```

## Company allowlist (optional)

By default the bot runs all configured sources. To run only a selected subset, set `JOB_COMPANIES` to a comma-separated list of company names.

Example:

```bash
JOB_COMPANIES="Amazon,Postman,Stripe" ./venv/bin/python main.py --once
```

## Notes

- The bot tracks already-posted jobs in local storage (see `utils/storage.py`), so you won’t get duplicates.
- The Discord webhook URL is read from `DISCORD_WEBHOOK_URL` (from real env vars or `.env`).

