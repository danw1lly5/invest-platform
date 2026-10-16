"""
Minimal NAV web API (fictional data).
The same code runs on AWS Lambda (lambda_handler) and locally (python -m app.api).
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.valuation import HOLDINGS, PRICES, calculate_nav, value_position


def get_nav():
    """Return the portfolio NAV and each position's value."""
    positions = [
        {
            "asset": asset,
            "quantity": qty,
            "price": PRICES[asset],
            "value": round(value_position(asset, qty, PRICES), 2),
        }
        for asset, qty in HOLDINGS.items()
    ]
    return {"currency": "SGD", "nav": calculate_nav(HOLDINGS, PRICES), "positions": positions}


ROUTES = {
    "/health": lambda: {"status": "ok"},
    "/nav": get_nav,
}


def route(path):
    """Look up the requested page; unknown pages get 404."""
    if path in ROUTES:
        return 200, ROUTES[path]()
    return 404, {"error": "not found"}


def lambda_handler(event, context):
    """Entry point when running on AWS Lambda."""
    status, body = route(event.get("rawPath", "/"))
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


class LocalHandler(BaseHTTPRequestHandler):
    """Entry point when running locally or inside the pipeline."""

    def do_GET(self):
        status, body = route(self.path)
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    print("NAV API running on http://localhost:8000  (Ctrl+C to stop)")
    HTTPServer(("0.0.0.0", 8000), LocalHandler).serve_forever()
