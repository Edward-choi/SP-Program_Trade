import requests
import time
import datetime
import pandas as pd
import ast
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_latest_timestamp(api_key, metric, asset='BTC', interval='24h'):
    """
    Fetch the latest timestamp from the Glassnode API for the given metric.
    Returns None on error or empty data.
    """
    url = f"https://api.glassnode.com/v1/metrics/{metric}"
    params = {
        'a': asset,
        'i': interval,
        'api_key': api_key,
        'f': 'JSON'
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            return data[-1]['t']
        else:
            return None
    except Exception as e:
        return None

# Load your API key
API_KEY = ""  # Replace with your key

# Load CSV
df = pd.read_csv('strategies.csv')

# Ensure output directory
os.makedirs('logs', exist_ok=True)

# Track last known timestamp for each unique (coin, endpoint, resolution)
last_seen = {}

# Cache for current loop: avoid duplicate API calls
current_cycle_cache = {}

while True:

    # Reset cache for this cycle
    current_cycle_cache.clear()

    # Collect all unique (coin, endpoint, resolution) to query
    to_query = set()

    for _, row in df.iterrows():
        try:
            endpoints_dict = ast.literal_eval(row['endpoints'])
        except:
            continue

        coin = row['coin']
        resolution = row['resolution']

        for key, endpoint in endpoints_dict.items():
            key_tuple = (coin, endpoint, resolution)
            to_query.add(key_tuple)

            # Initialize tracking if first time
            if key_tuple not in last_seen:
                last_seen[key_tuple] = None

    # === FETCH UNIQUE ENDPOINTS IN PARALLEL ===
    futures_to_cache_key = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        for coin, endpoint, resolution in to_query:
            cache_key = (coin, endpoint, resolution)
            future = executor.submit(get_latest_timestamp, API_KEY, endpoint, asset=coin, interval=resolution)
            futures_to_cache_key[future] = cache_key

        for future in as_completed(futures_to_cache_key):
            latest_t = future.result()
            cache_key = futures_to_cache_key[future]
            current_cycle_cache[cache_key] = latest_t

    # === PROCESS RESULTS ===
    for coin, endpoint, resolution in to_query:
        cache_key = (coin, endpoint, resolution)
        latest_t = current_cycle_cache.get(cache_key)
        if latest_t is None:
            continue

        dt_latest = datetime.datetime.fromtimestamp(latest_t, tz=datetime.timezone.utc)
        current_time = time.time()
        dt_current = datetime.datetime.fromtimestamp(current_time, tz=datetime.timezone.utc)
        delay = current_time - latest_t - 3600  # Adjust for 1 hour offset

        # Create log file
        safe_endpoint = endpoint.replace('/', '_')
        log_filename = f"logs/{coin}-{safe_endpoint}-{resolution}.log"

        # Log current state
        with open(log_filename, 'a') as f:
            f.write(f"{dt_current.isoformat()} | {dt_latest.isoformat()} | {delay:.2f}s\n")

        # Detect update
        prev_t = last_seen[cache_key]
        if prev_t is not None and latest_t > prev_t:
            with open(log_filename, 'a') as f:
                f.write(f"UPDATE DETECTED | {dt_latest.isoformat()}\n")

        last_seen[cache_key] = latest_t

    # === END OF LOOP: Wait 1 minute ===
    time.sleep(60)
