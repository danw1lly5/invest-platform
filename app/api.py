"""
Minimal NAV web API (fictional data).
The same code runs on AWS Lambda (lambda_handler) and locally (python -m app.api).
"""
import json
import os
import os
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


# Sent with EVERY response (found missing by the ZAP DAST scan)
SECURITY_HEADERS = {
    "Content-Type": "application/json",
    "X-Content-Type-Options": "nosniff",
    "Cache-Control": "no-store",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'; form-action 'none'",
}

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
        "headers": dict(SECURITY_HEADERS),
        "body": json.dumps(body),
    }


class LocalHandler(BaseHTTPRequestHandler):
    """Entry point when running locally or inside the pipeline."""

    def version_string(self):
        """Do not reveal server software or version to visitors."""
        return "NAV-API"

    def do_GET(self):
        status, body = route(self.path)
        payload = json.dumps(body).encode()
        self.send_response(status)
        for name, value in SECURITY_HEADERS.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    print("NAV API running on http://localhost:8000  (Ctrl+C to stop)")
    host = os.environ.get("NAV_BIND_HOST", "127.0.0.1")
    HTTPServer((host, 8000), LocalHandler).serve_forever()
