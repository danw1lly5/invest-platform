"""Management fee calculation (fictional)."""

# Annual management fee RATE - this is DATA, not code.
# Changes to the rate go through maker-checker, never through free-text formulas.
ANNUAL_FEE_RATE = 0.0075   # 0.75% per year

MIN_RATE = 0.0
MAX_RATE = 0.02            # policy cap: 2% per year


def monthly_fee(nav, annual_rate=ANNUAL_FEE_RATE):
    """Monthly fee = NAV x annual rate / 12. The rate is validated, never executed."""
    rate = float(annual_rate)          # text that is not a plain number is rejected here
    if not MIN_RATE <= rate <= MAX_RATE:
        raise ValueError(f"Fee rate {rate} outside approved range {MIN_RATE}-{MAX_RATE}")
    return round(nav * rate / 12, 2)
