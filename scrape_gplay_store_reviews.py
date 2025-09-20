import sys
import json
from datetime import datetime, timedelta
from google_play_scraper import reviews, Sort

# --- Input ---
app_id = sys.argv[1]
country = sys.argv[2]

# --- Constants ---
REVIEW_LIMIT = 5000
MIN_REVIEW_LENGTH = 100
YEARS_BACK = 1

# --- Time filter ---
cutoff_date = datetime.now() - timedelta(days=YEARS_BACK * 365)

# --- Output structure ---
data = {country: {i: [] for i in range(1, 6)}}

# print(f"\nFetching reviews for {app_id} in country: {country}")

continuation_token = None
fetched = 0

while fetched < REVIEW_LIMIT:
    result, continuation_token = reviews(
        app_id,
        lang="en",
        country=country,
        sort=Sort.NEWEST,
        count=100,
        continuation_token=continuation_token
    )

    if not result:
        break

    for r in result:
        review_date = r["at"]
        review_text = r["content"]

        if review_date >= cutoff_date and len(review_text) >= MIN_REVIEW_LENGTH:
            rating = r["score"]  # 1 to 5
            data[country][rating].append(review_text)

    fetched += len(result)
    # print(f"Fetched {fetched} reviews so far for {country}...")

    if continuation_token is None:
        break

# --- Save as JSON ---
with open(f"{country}_reviews.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# --- Optional: print JSON to terminal ---
print(json.dumps(data, indent=4, ensure_ascii=False))
