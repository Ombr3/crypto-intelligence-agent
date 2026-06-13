import requests

BASE_URL = "https://fapi.binance.com"

def get_funding_rate(symbol: str) -> dict:
    """Get the latest funding rate for a futures symbol e.g. ETHUSDT"""
    url = f"{BASE_URL}/fapi/v1/fundingRate"
    params = {"symbol": symbol, "limit": 1}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        "symbol": symbol,
        "funding_rate": float(data[0]["fundingRate"]) * 100,  # convert to %
        "funding_time": data[0]["fundingTime"]
    }

def get_open_interest(symbol: str) -> dict:
    """Get current open interest for a futures symbol"""
    url = f"{BASE_URL}/fapi/v1/openInterest"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        "symbol": symbol,
        "open_interest": float(data["openInterest"])
    }

def get_price(symbol: str) -> dict:
    """Get current mark price"""
    url = f"{BASE_URL}/fapi/v1/premiumIndex"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        "symbol": symbol,
        "mark_price": float(data["markPrice"])
    }

if __name__ == "__main__":
    symbol = "ETHUSDT"
    print(get_funding_rate(symbol))
    print(get_open_interest(symbol))
    print(get_price(symbol))
