"""Management fee calculation (fictional)."""

# Fee formula maintained by the operations team, e.g. "nav * 0.0075 / 12"
FEE_FORMULA = "nav * 0.0075 / 12"


def monthly_fee(nav, formula=FEE_FORMULA):
    """Apply the configured fee formula to the NAV."""
    return round(eval(formula, {"nav": nav}), 2)
