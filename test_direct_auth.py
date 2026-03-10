"""
Direct Delta India API test - bypasses CCXT completely
Uses Delta's own official signature method
"""
import hashlib
import hmac
import time
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY    = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_SECRET_KEY")

BASE_URL = "https://api.india.delta.exchange"

def generate_signature(secret, method, endpoint, query_string, payload, timestamp):
    message = method + timestamp + endpoint + query_string + payload
    mac = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        digestmod=hashlib.sha256
    )
    return mac.hexdigest()

print("=" * 55)
print("  Delta India — Direct API Auth Test")
print("=" * 55)
print(f"  Key    : {API_KEY[:6] if API_KEY else 'NONE'}...{API_KEY[-4:] if API_KEY else ''}")
print(f"  Secret : {API_SECRET[:6] if API_SECRET else 'NONE'}...{API_SECRET[-4:] if API_SECRET else ''}")
print()

# Test 1: Public (no auth)
print("Test 1: Public API (no auth needed)...")
try:
    r = requests.get(f"{BASE_URL}/v2/products", timeout=10)
    if r.status_code == 200:
        print(f"  ✅ Public API OK — Delta India is reachable")
    else:
        print(f"  ❌ Status {r.status_code}: {r.text[:200]}")
except Exception as e:
    print(f"  ❌ Network error: {e}")

print()

# Test 2: Private (auth required)
print("Test 2: Private API (auth test)...")
try:
    endpoint     = "/v2/wallet/balances"
    method       = "GET"
    timestamp    = str(int(time.time()))

    signature = generate_signature(API_SECRET, method, endpoint, "", "", timestamp)

    headers = {
        "api-key":      API_KEY,
        "timestamp":    timestamp,
        "signature":    signature,
        "Content-Type": "application/json"
    }

    r = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
    print(f"  HTTP Status : {r.status_code}")

    data = r.json()
    print(f"  Raw Response: {json.dumps(data)[:300]}")
    print()

    if r.status_code == 200 and data.get("success"):
        print("  ✅ PRIVATE API WORKS! Your key is valid.")
        for b in data.get("result", []):
            if b.get("asset_symbol") in ["USDT", "BTC", "ETH"]:
                print(f"  💰 {b['asset_symbol']}: {b.get('available_balance', 0)}")
    else:
        error_code = data.get("error", {}).get("code", "unknown")
        print(f"  ❌ Auth failed — Error code: [{error_code}]")
        print()
        print("  DIAGNOSIS:")
        print("  1. Key from TESTNET portal? → testnet.india.delta.exchange")
        print("  2. Key from GLOBAL portal?  → delta.exchange (not India)")
        print("  3. Key deleted/expired on portal?")
        print("  4. IP whitelist blocking you?")
        print()
        print("  FIX: india.delta.exchange → API Keys → Delete → Create fresh")
        print("       Enable: Read + Trading | No IP whitelist")

except Exception as e:
    print(f"  ❌ Exception: {e}")

print()
print("=" * 55)
