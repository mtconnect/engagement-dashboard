import requests
import os
import json
import csv
from datetime import datetime
from collections import defaultdict

# ==========================
# CONFIG
# ==========================
OWNER = "mtconnect"          # change if needed
REPO = "cppagent"            # change to target repo
DATA_DIR = "data/stars"
RAW_FILE = f"{DATA_DIR}/stars_raw.json"
DAILY_FILE = f"{DATA_DIR}/stars_daily.csv"

TOKEN = os.getenv("GH_TOKEN")

headers = {
    "Accept": "application/vnd.github.star+json",
    "Authorization": f"Bearer {TOKEN}"
}

def fetch_all_stars():
    stars = []
    page = 1

    while True:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/stargazers"
        params = {"per_page": 100, "page": page}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        stars.extend(data)
        page += 1

    return stars

def save_raw(stars):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RAW_FILE, "w") as f:
        json.dump(stars, f, indent=2)

def generate_daily_csv(stars):
    daily_counts = defaultdict(int)

    for star in stars:
        date = star["starred_at"][:10]
        daily_counts[date] += 1

    sorted_dates = sorted(daily_counts.keys())

    total = 0
    rows = []

    for date in sorted_dates:
        total += daily_counts[date]
        rows.append([date, daily_counts[date], total])

    with open(DAILY_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "stars_added", "total_stars"])
        writer.writerows(rows)

def main():
    stars = fetch_all_stars()
    save_raw(stars)
    generate_daily_csv(stars)

if __name__ == "__main__":
    main()
