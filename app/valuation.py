"""
Portfolio valuation module (fictional data).
Calculates the portfolio's Net Asset Value (NAV):
the total market value of everything the fund holds.
"""

# HOLDINGS: how many units of each asset the fund owns
HOLDINGS = {
    "ALPHA_TECH": 1_000,        # listed share  (public markets)
    "BETA_BANK": 2_500,         # listed share  (public markets)
    "GAMMA_INFRA_FUND": 10,     # fund units    (private markets)
}

# PRICES: latest price per unit, in SGD
PRICES = {
    "ALPHA_TECH": 152.40,
    "BETA_BANK": 39.10,
    "GAMMA_INFRA_FUND": 27_000.00,   # private assets are valued periodically, not traded daily
}


def value_position(asset, quantity, prices):
    """Value one holding: quantity x price. Stop if the price is missing or invalid."""
    if asset not in prices:
        raise ValueError(f"No price for {asset} - cannot value the portfolio")
    price = prices[asset]
    if price <= 0:
        raise ValueError(f"Invalid price for {asset}: {price}")
    return quantity * price


def calculate_nav(holdings, prices):
    """Add up the value of every holding."""
    total = 0.0
    for asset, quantity in holdings.items():
        total += value_position(asset, quantity, prices)
    return round(total, 2)


if __name__ == "__main__":
    for asset, qty in HOLDINGS.items():
        value = value_position(asset, qty, PRICES)
        print(f"{asset:<18} {qty:>6,} units x {PRICES[asset]:>10,.2f} = SGD {value:>12,.2f}")
    print("-" * 64)
    print(f"Portfolio NAV: SGD {calculate_nav(HOLDINGS, PRICES):,.2f}")