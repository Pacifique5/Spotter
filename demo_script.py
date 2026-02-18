#!/usr/bin/env python
"""
Demo script to test the Fuel Route Optimizer API.
Run this after starting the Django server.
"""

import requests
import json
import sys


def test_route(start, finish):
    """Test a route and display results."""
    print(f"\n{'='*60}")
    print(f"Testing route: {start} → {finish}")
    print('='*60)
    
    url = 'http://localhost:8000/api/route/'
    data = {'start': start, 'finish': finish}
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✓ Route calculated successfully!")
            print(f"\nStart: {result['start']['name']}")
            print(f"Finish: {result['finish']['name']}")
            
            summary = result['summary']
            print(f"\n--- Summary ---")
            print(f"Total Distance: {summary['total_distance_miles']} miles")
            print(f"Total Fuel Needed: {summary['total_fuel_gallons']} gallons")
            print(f"Total Fuel Cost: ${summary['total_fuel_cost_usd']}")
            print(f"Vehicle MPG: {summary['vehicle_mpg']}")
            print(f"Vehicle Range: {summary['vehicle_range_miles']} miles")
            
            fuel_stops = result['fuel_stops']
            if fuel_stops:
                print(f"\n--- Fuel Stops ({len(fuel_stops)}) ---")
                for stop in fuel_stops:
                    print(f"\nStop #{stop['stop_number']}:")
                    print(f"  Location: {stop['location']['state']}")
                    print(f"  Distance from start: {stop['distance_from_start_miles']} miles")
                    print(f"  Fuel price: ${stop['fuel_price_per_gallon']}/gallon")
                    print(f"  Gallons to refuel: {stop['gallons_to_refuel']}")
                    print(f"  Cost at stop: ${stop['cost_at_stop']}")
            else:
                print("\n✓ No fuel stops needed - destination within range!")
            
            return True
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(response.json())
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to server.")
        print("Make sure Django server is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Run demo tests."""
    print("\n" + "="*60)
    print("Fuel Route Optimizer API - Demo Script")
    print("="*60)
    
    # Test cases
    test_cases = [
        ("Boston, MA", "New York, NY"),  # Short route
        ("New York, NY", "Chicago, IL"),  # Medium route
        ("New York, NY", "Los Angeles, CA"),  # Long route
    ]
    
    results = []
    for start, finish in test_cases:
        success = test_route(start, finish)
        results.append(success)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print('='*60)
    
    if all(results):
        print("\n✓ All tests passed! API is working correctly.")
        return 0
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
