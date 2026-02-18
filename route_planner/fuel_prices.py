import csv
import os
from django.conf import settings

# Cache for fuel prices loaded from CSV
_FUEL_PRICES_CACHE = None
_TRUCK_STOPS_CACHE = None


def _load_fuel_data():
    """Load fuel price data from CSV file."""
    global _FUEL_PRICES_CACHE, _TRUCK_STOPS_CACHE
    
    if _FUEL_PRICES_CACHE is not None:
        return _FUEL_PRICES_CACHE, _TRUCK_STOPS_CACHE
    
    # Path to CSV file
    csv_path = os.path.join(settings.BASE_DIR, 'fuel-prices-for-be-assessment.csv')
    
    truck_stops = []
    state_prices = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    state = row['State'].strip()
                    price = float(row['Retail Price'])
                    
                    # Store truck stop data
                    truck_stops.append({
                        'id': row['OPIS Truckstop ID'],
                        'name': row['Truckstop Name'],
                        'address': row['Address'],
                        'city': row['City'],
                        'state': state,
                        'price': price
                    })
                    
                    # Calculate average price per state
                    if state not in state_prices:
                        state_prices[state] = []
                    state_prices[state].append(price)
                    
                except (ValueError, KeyError) as e:
                    continue
        
        # Calculate average prices per state
        _FUEL_PRICES_CACHE = {
            state: round(sum(prices) / len(prices), 3)
            for state, prices in state_prices.items()
        }
        _TRUCK_STOPS_CACHE = truck_stops
        
    except FileNotFoundError:
        # Fallback to default prices if CSV not found
        _FUEL_PRICES_CACHE = {'US': 3.00}
        _TRUCK_STOPS_CACHE = []
    
    return _FUEL_PRICES_CACHE, _TRUCK_STOPS_CACHE


def get_fuel_price(state_code):
    """Get average fuel price for a given state code from CSV data."""
    fuel_prices, _ = _load_fuel_data()
    return fuel_prices.get(state_code.upper(), 3.00)


def get_truck_stops_by_state(state_code):
    """Get all truck stops for a given state."""
    _, truck_stops = _load_fuel_data()
    return [stop for stop in truck_stops if stop['state'] == state_code.upper()]


def get_all_truck_stops():
    """Get all truck stops from CSV data."""
    _, truck_stops = _load_fuel_data()
    return truck_stops
