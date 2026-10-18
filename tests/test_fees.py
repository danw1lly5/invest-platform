"""Integrity checks for the management fee."""
import pytest

from app.fees import monthly_fee


def test_monthly_fee_on_approved_nav():
    """0.75% a year on NAV 500,150 = 312.59 a month."""
    assert monthly_fee(500150.00) == 312.59


def test_rate_above_policy_cap_rejected():
    """A rate above the 2% cap must be refused."""
    with pytest.raises(ValueError):
        monthly_fee(500150.00, annual_rate=0.5)


def test_text_instead_of_number_rejected():
    """Anything that is not a plain number must be refused, never executed."""
    with pytest.raises(ValueError):
        monthly_fee(500150.00, annual_rate="nav * 0.0075 / 12")
