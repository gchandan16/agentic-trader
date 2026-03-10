import ccxt
import hmac
import hashlib
import time
import requests
import json

from config.settings import API_KEY, SECRET_KEY
from logs.logger import logger

BASE_URL = "https://api.india.delta.exchange"


class DeltaClient:
    """
    Hybrid client:
    - CCXT for PUBLIC calls (market data, candles, ticker)
    - Direct REST for PRIVATE calls (orders, balance, positions)
    
    Reason: CCXT generates wrong signatures for Delta India private API.
    Direct REST using Delta's official HMAC-SHA256 method works correctly.
    """

    def __init__(self):
        try:
            # CCXT only for public market data
            self.exchange = ccxt.delta({
                "apiKey": API_KEY,
                "secret": SECRET_KEY,
                "enableRateLimit": True,
                "hostname": "api.india.delta.exchange",
                "options": {"adjustForTimeDifference": True}
            })

            self.api_key    = API_KEY
            self.api_secret = SECRET_KEY
            self.session    = requests.Session()
            self.session.headers.update({"Content-Type": "application/json"})

            logger.info("DeltaClient initialized (hybrid mode)")
            print("✅ DeltaClient ready")

        except Exception as e:
            logger.error(f"Exchange Init Failed: {e}")
            raise e

    # ──────────────────────────────────────────────
    # PRIVATE: Signature generator (official Delta method)
    # ──────────────────────────────────────────────
    def _sign(self, method, endpoint, query_string="", payload=""):
        timestamp = str(int(time.time()))
        message   = method + timestamp + endpoint + query_string + payload
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            digestmod=hashlib.sha256
        ).hexdigest()
        return timestamp, signature

    def _private_get(self, endpoint, params=None):
        query_string = ""
        if params:
            query_string = "?" + "&".join(f"{k}={v}" for k, v in params.items())

        timestamp, signature = self._sign("GET", endpoint, query_string)

        headers = {
            "api-key":      self.api_key,
            "timestamp":    timestamp,
            "signature":    signature,
            "Content-Type": "application/json"
        }

        url = BASE_URL + endpoint + query_string
        r   = self.session.get(url, headers=headers, timeout=10)
        return r.json()

    def _private_post(self, endpoint, body: dict):
        payload   = json.dumps(body, separators=(",", ":"))
        timestamp, signature = self._sign("POST", endpoint, "", payload)

        headers = {
            "api-key":      self.api_key,
            "timestamp":    timestamp,
            "signature":    signature,
            "Content-Type": "application/json"
        }

        url = BASE_URL + endpoint
        r   = self.session.post(url, headers=headers, data=payload, timeout=10)
        return r.json()

    def _private_delete(self, endpoint, body: dict = None):
        payload   = json.dumps(body or {}, separators=(",", ":"))
        timestamp, signature = self._sign("DELETE", endpoint, "", payload)

        headers = {
            "api-key":      self.api_key,
            "timestamp":    timestamp,
            "signature":    signature,
            "Content-Type": "application/json"
        }

        url = BASE_URL + endpoint
        r   = self.session.delete(url, headers=headers, data=payload, timeout=10)
        return r.json()

    # ──────────────────────────────────────────────
    # PUBLIC: Market data via CCXT
    # ──────────────────────────────────────────────
    def get_price(self, symbol="BTC/USDT:USDT"):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker["last"]
        except Exception as e:
            logger.error(f"Price fetch error: {e}")
            return None

    def fetch_candles(self, symbol="BTC/USDT:USDT", timeframe="5m", limit=50):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as e:
            logger.error(f"Candle fetch error: {e}")
            return None

    # ──────────────────────────────────────────────
    # PRIVATE: Account
    # ──────────────────────────────────────────────
    def get_balance(self):
        """Returns USDT available balance"""
        try:
            data = self._private_get("/v2/wallet/balances")
            if not data.get("success"):
                logger.error(f"Balance fetch failed: {data}")
                return None

            for asset in data.get("result", []):
                if asset.get("asset_symbol") == "USDT":
                    balance = float(asset.get("available_balance", 0))
                    logger.info(f"USDT Balance: {balance}")
                    return balance

            return 0.0

        except Exception as e:
            logger.error(f"Balance error: {e}")
            return None

    def get_positions(self):
        """Returns open positions"""
        try:
            data = self._private_get("/v2/positions/margined")
            if data.get("success"):
                return data.get("result", [])
            logger.error(f"Positions fetch failed: {data}")
            return []
        except Exception as e:
            logger.error(f"Positions error: {e}")
            return []

    # ──────────────────────────────────────────────
    # PRIVATE: Orders
    # ──────────────────────────────────────────────
    def place_market_order(self, product_symbol, side, size):
        """
        Place a market order.
        product_symbol: e.g. "BTCUSDT" (Delta format, not CCXT format)
        side          : "buy" or "sell"
        size          : quantity in contracts
        """
        try:
            body = {
                "product_symbol": product_symbol,
                "side":           side,
                "order_type":     "market_order",
                "size":           int(size),
            }

            logger.info(f"Placing market order: {body}")
            data = self._private_post("/v2/orders", body)

            if data.get("success"):
                order = data.get("result", {})
                logger.info(f"Order placed successfully: {order.get('id')}")
                print(f"✅ Order placed! ID: {order.get('id')} | Side: {side} | Size: {size}")
                return order
            else:
                logger.error(f"Order failed: {data}")
                print(f"❌ Order failed: {data}")
                return None

        except Exception as e:
            logger.error(f"Order placement error: {e}")
            print(f"❌ Order exception: {e}")
            return None

    def place_limit_order(self, product_symbol, side, size, limit_price):
        """Place a limit order"""
        try:
            body = {
                "product_symbol": product_symbol,
                "side":           side,
                "order_type":     "limit_order",
                "size":           int(size),
                "limit_price":    str(limit_price),
            }

            data = self._private_post("/v2/orders", body)

            if data.get("success"):
                order = data.get("result", {})
                logger.info(f"Limit order placed: {order.get('id')}")
                return order
            else:
                logger.error(f"Limit order failed: {data}")
                return None

        except Exception as e:
            logger.error(f"Limit order error: {e}")
            return None

    def cancel_order(self, order_id, product_id):
        """Cancel an open order"""
        try:
            body = {"id": order_id, "product_id": product_id}
            data = self._private_delete("/v2/orders", body)

            if data.get("success"):
                logger.info(f"Order {order_id} cancelled")
                return True
            else:
                logger.error(f"Cancel failed: {data}")
                return False

        except Exception as e:
            logger.error(f"Cancel error: {e}")
            return False

    def get_open_orders(self, product_symbol=None):
        """Get all open orders"""
        try:
            params = {}
            if product_symbol:
                params["product_symbol"] = product_symbol

            data = self._private_get("/v2/orders", params)

            if data.get("success"):
                return data.get("result", {}).get("open_orders", [])
            return []

        except Exception as e:
            logger.error(f"Open orders error: {e}")
            return []

    # ──────────────────────────────────────────────
    # AUTH TEST
    # ──────────────────────────────────────────────
    def test_auth(self):
        """Quick auth check — call this on startup"""
        balance = self.get_balance()
        if balance is not None:
            print(f"✅ Auth OK — USDT Balance: {balance}")
            return True
        else:
            print("❌ Auth FAILED — check API key and permissions")
            return False
