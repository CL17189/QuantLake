import requests
import time
import os
import json
from datetime import datetime
from config import API_KEY, SYMBOLS, BASE_URL

def fetch_quote(symbol):
    url = f"{BASE_URL}/quote"
    params = {"symbol": symbol, "token": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_profile(symbol):
    url = f"{BASE_URL}/stock/profile2"
    params = {"symbol": symbol, "token": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_data(symbol, quote_data, profile_data, output_dir="../data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{symbol}_{timestamp}.json"
    full_path = os.path.join(output_dir, filename)

    data = {
        "symbol": symbol,
        "timestamp": timestamp,
        "quote": quote_data,
        "profile": profile_data
    }

    with open(full_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved: {full_path}")

def main():
    print("🔍 Start fetching stock data...")
    for symbol in SYMBOLS:
        try:
            quote = fetch_quote(symbol)
            profile = fetch_profile(symbol)
            save_data(symbol, quote, profile)
            time.sleep(1)  # Respect rate limit
        except Exception as e:
            print(f"❌ Failed to fetch {symbol}: {e}")

if __name__ == "__main__":
    main()
