"""Connector to the external pricing vendor (fictional)."""
import os

PRICING_VENDOR_URL = "https://api.example-prices.com/v1/quotes"


def get_api_key():
    """Read the key at runtime from the environment (injected from a vault), never from code."""
    key = os.environ.get("PRICING_VENDOR_API_KEY")
    if not key:
        raise RuntimeError("PRICING_VENDOR_API_KEY is not set")
    return key


def fetch_prices():
    """Placeholder: would call the vendor API using get_api_key()."""
    return {}
