# Setup and Usage Guide

Complete step-by-step instructions to set up and run the Fuel Route Optimizer API.

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenRouteService API key (free)

---

## Step 1: Get OpenRouteService API Key

1. Go to https://openrouteservice.org/dev/#/signup
2. Sign up for a free account
3. Copy your API key (it will look like: `eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6...`)

---

## Step 2: Install Dependencies

### Option A: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Global Installation

```bash
pip install -r requirements.txt
```

---

## Step 3: Configure API Key

Create a `.env` file in the project root:

```bash
# On Windows:
echo OPENROUTE_API_KEY=your_api_key_here > .env

# On Mac/Linux:
echo "OPENROUTE_API_KEY=your_api_key_here" > .env
```

Or manually create `.env` file with this content:
```
OPENROUTE_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key from Step 1.

---

## Step 4: Run Database Migrations

```bash
python manage.py migrate
```

This creates the SQLite database (required by Django, but not used for fuel data).

---

## Step 5: Start the Server

```bash
python manage.py runserver
```

Server will start at: **http://127.0.0.1:8000**

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## Step 6: Test the API

### Using cURL (Command Line)

**Short Route Test:**
```bash
curl -X POST http://127.0.0.1:8000/api/route/ ^
  -H "Content-Type: application/json" ^
  -d "{\"start\": \"Boston, MA\", \"finish\": \"New York, NY\"}"
```

**Long Route Test:**
```bash
curl -X POST http://127.0.0.1:8000/api/route/ ^
  -H "Content-Type: application/json" ^
  -d "{\"start\": \"New York, NY\", \"finish\": \"Los Angeles, CA\"}"
```

### Using Python

Create a test file `test_api.py`:
```python
import requests
import json

response = requests.post('http://127.0.0.1:8000/api/route/', json={
    'start': 'New York, NY',
    'finish': 'Los Angeles, CA'
})

print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
```

Run it:
```bash
python test_api.py
```

### Using Postman

1. Open Postman
2. Import the file: `postman_collection.json`
3. You'll see 3 pre-configured requests:
   - Short Route (Boston → New York)
   - Long Route (New York → Los Angeles)
   - Cross-Country (Miami → Seattle)
4. Click "Send" on any request to test

---

## API Usage

### Endpoint

**POST** `/api/route/`

### Request Format

```json
{
  "start": "New York, NY",
  "finish": "Los Angeles, CA"
}
```

Both `start` and `finish` must be valid US locations (city, state format recommended).

### Response Format

```json
{
  "start": {
    "name": "New York, NY, USA",
    "coordinates": {"lat": 40.7128, "lon": -74.0060},
    "state": "NY"
  },
  "finish": {
    "name": "Los Angeles, CA, USA",
    "coordinates": {"lat": 34.0522, "lon": -118.2437},
    "state": "CA"
  },
  "route": {
    "geometry": { /* GeoJSON geometry for map display */ },
    "duration_seconds": 142560
  },
  "fuel_stops": [
    {
      "stop_number": 1,
      "distance_from_start_miles": 500.0,
      "state": "OH",
      "fuel_price_per_gallon": 3.15,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 157.50
    }
    // ... more stops
  ],
  "summary": {
    "total_distance_miles": 2789.45,
    "total_fuel_gallons": 278.95,
    "total_fuel_cost_usd": 856.32,
    "vehicle_mpg": 10,
    "vehicle_range_miles": 500
  }
}
```

### Response Fields

- **start/finish**: Location details with coordinates
- **route.geometry**: GeoJSON geometry for displaying route on a map
- **route.duration_seconds**: Estimated travel time
- **fuel_stops**: Array of recommended fuel stops
  - Stops are calculated every 500 miles (vehicle range)
  - Each stop includes location, fuel price, and cost
  - Prices are real data from 8,151 truck stops (CSV file)
- **summary**: Total distance, fuel consumption, and cost

---

## How It Works

1. **Geocoding**: Converts location names to GPS coordinates using OpenRouteService
2. **Routing**: Gets optimal driving route with distance and geometry
3. **Fuel Calculation**:
   - Loads real fuel prices from `fuel-prices-for-be-assessment.csv` (8,151 truck stops)
   - Calculates state-averaged prices
   - Determines fuel stops every 500 miles (vehicle range)
   - Computes fuel cost using 10 MPG efficiency
4. **Response**: Returns complete route with fuel stops and total cost

---

## Project Structure

```
fuel_route_api/
├── fuel_route_api/              # Django project settings
│   ├── settings.py              # Configuration
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI config
├── route_planner/               # Main application
│   ├── views.py                 # API endpoint
│   ├── services.py              # Route calculation logic
│   ├── fuel_prices.py           # CSV data loader
│   ├── serializers.py           # Request validation
│   └── urls.py                  # App URLs
├── fuel-prices-for-be-assessment.csv  # Real fuel price data
├── .env                         # API key (create this)
├── .env.example                 # Example .env file
├── requirements.txt             # Python dependencies
├── manage.py                    # Django CLI
├── postman_collection.json      # Postman test collection
├── README.md                    # Project overview
└── SETUP.md                     # This file
```

---

## Troubleshooting

### Server won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`

### API returns 500 error
- Verify `.env` file exists with valid API key
- Check that `fuel-prices-for-be-assessment.csv` exists in project root
- Look at server console for error details

### API returns 404 for location
- Make sure location is in the USA
- Use format: "City, State" (e.g., "New York, NY")
- Try more specific location names

### Slow response times
- First request may be slower (loading CSV data)
- Subsequent requests are faster (data is cached)
- Long routes (cross-country) take longer to calculate

---

## Quick Reference Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Test API (Windows)
curl -X POST http://127.0.0.1:8000/api/route/ ^
  -H "Content-Type: application/json" ^
  -d "{\"start\": \"New York, NY\", \"finish\": \"Boston, MA\"}"

# Test API (Mac/Linux)
curl -X POST http://127.0.0.1:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d '{"start": "New York, NY", "finish": "Boston, MA"}'
```

---

## Technical Details

- **Django**: 5.0.2
- **Django REST Framework**: 3.14.0
- **Python**: 3.8+
- **Database**: SQLite (for Django, not used for fuel data)
- **External API**: OpenRouteService (free tier)
- **Fuel Data**: 8,151 truck stops from CSV file
- **Vehicle Specs**: 10 MPG, 500-mile range

---

## Assignment Requirements Met

✓ Django latest stable version (5.0.2)  
✓ Takes start and finish locations (US only)  
✓ Returns route map with geometry  
✓ Optimal fuel stops based on cost  
✓ 500-mile vehicle range  
✓ 10 MPG fuel efficiency  
✓ Uses provided CSV file (8,151 truck stops)  
✓ Free routing API (OpenRouteService)  
✓ Minimal API calls (2-3 per request)  
✓ Fast response times  

---

## Support

For issues or questions, check:
1. This setup guide
2. README.md for project overview
3. Server console output for error messages
4. OpenRouteService API status: https://openrouteservice.org/dev/#/home
