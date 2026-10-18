"""Automated checks that run on every pull request."""
import json

import pytest

from app.api import lambda_handler
from app.valuation import HOLDINGS, PRICES, calculate_nav, value_position


def test_nav_matches_approved_value():
    """Integrity check: NAV must equal the last approved figure."""
    assert calculate_nav(HOLDINGS, PRICES) == 500150.00


def test_missing_price_fails_loudly():
    """A missing price must stop the valuation, never count as zero."""
    with pytest.raises(ValueError):
        value_position("UNKNOWN_ASSET", 10, PRICES)


def test_zero_or_negative_price_rejected():
    """A zero or negative price must be rejected."""
    with pytest.raises(ValueError):
        value_position("ALPHA_TECH", 10, {"ALPHA_TECH": 0})


def test_api_health_endpoint():
    """The service answers its health check."""
    response = lambda_handler({"rawPath": "/health"}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"status": "ok"}


def test_api_nav_endpoint():
    """The API returns the same NAV as the valuation engine."""
    response = lambda_handler({"rawPath": "/nav"}, None)
    assert json.loads(response["body"])["nav"] == 500150.00


def test_security_headers_present():
    """Hardening found by DAST must not silently disappear."""
    headers = lambda_handler({"rawPath": "/nav"}, None)["headers"]
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["Cache-Control"] == "no-store"
