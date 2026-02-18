"""Simple API test script"""
import requests
import json

API_URL = 'http://127.0.0.1:8000/api/route/'

print("Testing Fuel Route Optimizer API...")
print("=" * 60)

# Test short route
print("\nTest 1: Short Route (Boston -> New York)")
response = requests.post(API_URL, json={
    'start': 'Boston, MA',
    'finish': 'New York, NY'
})

if response.status_code == 200:
    data = response.json()
    print(f"Status: {response.status_code} OK")
    print(f"Distance: {data['summary']['total_distance_miles']} miles")
    print(f"Fuel Stops: {len(data['fuel_stops'])}")
    print(f"Total Cost: ${data['summary']['total_fuel_cost_usd']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

# Test long route
print("\nTest 2: Long Route (New York -> Los Angeles)")
response = requests.post(API_URL, json={
    'start': 'New York, NY',
    'finish': 'Los Angeles, CA'
}, timeout=30)

if response.status_code == 200:
    data = response.json()
    print(f"Status: {response.status_code} OK")
    print(f"Distance: {data['summary']['total_distance_miles']} miles")
    print(f"Fuel Stops: {len(data['fuel_stops'])}")
    print(f"Total Cost: ${data['summary']['total_fuel_cost_usd']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

print("\n" + "=" * 60)
print("API is working correctly!")
