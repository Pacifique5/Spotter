# Fuel prices data (price per gallon in USD)
# Format: {state_code: price_per_gallon}
FUEL_PRICES = {
    'AL': 2.89, 'AK': 3.45, 'AZ': 3.12, 'AR': 2.78, 'CA': 4.65,
    'CO': 3.05, 'CT': 3.28, 'DE': 3.15, 'FL': 3.02, 'GA': 2.92,
    'HI': 4.58, 'ID': 3.35, 'IL': 3.42, 'IN': 3.18, 'IA': 2.95,
    'KS': 2.88, 'KY': 2.95, 'LA': 2.75, 'ME': 3.22, 'MD': 3.25,
    'MA': 3.35, 'MI': 3.28, 'MN': 3.05, 'MS': 2.72, 'MO': 2.85,
    'MT': 3.18, 'NE': 2.98, 'NV': 3.85, 'NH': 3.18, 'NJ': 3.38,
    'NM': 2.95, 'NY': 3.52, 'NC': 3.05, 'ND': 3.12, 'OH': 3.15,
    'OK': 2.82, 'OR': 3.75, 'PA': 3.58, 'RI': 3.32, 'SC': 2.88,
    'SD': 3.08, 'TN': 2.85, 'TX': 2.68, 'UT': 3.28, 'VT': 3.35,
    'VA': 3.08, 'WA': 3.95, 'WV': 3.12, 'WI': 3.05, 'WY': 3.15,
    'DC': 3.42
}

def get_fuel_price(state_code):
    """Get fuel price for a given state code."""
    return FUEL_PRICES.get(state_code.upper(), 3.00)
