# Fuel Route Optimizer API

Django REST API that calculates optimal fuel stops along a route based on fuel prices.

## Features
- Route planning between US locations
- Optimal fuel stop recommendations based on price
- Total fuel cost calculation (10 MPG vehicle, 500-mile range)
- Fast response times with minimal external API calls (1-2 API calls total)
- Uses OpenRouteService for routing and geocoding

## Setup

### Quick Setup (Recommended)
```bash
python setup.py
```

### Manual Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a free API key from [OpenRouteService](https://openrouteservice.org/dev/#/signup)

3. Create `.env` file in project root:
```
OPENROUTE_API_KEY=your_api_key_here
```

4. Run migrations and start server:
```bash
python manage.py migrate
python manage.py runserver
```

Server will be available at `http://localhost:8000`

## API Endpoint

POST `/api/route/`

Request body:
```json
{
  "start": "New York, NY",
  "finish": "Los Angeles, CA"
}
```

Response:
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
    "geometry": {...},
    "duration_seconds": 142560
  },
  "fuel_stops": [
    {
      "stop_number": 1,
      "location": {"lat": 39.95, "lon": -82.99, "state": "OH"},
      "distance_from_start_miles": 500,
      "fuel_price_per_gallon": 3.15,
      "gallons_to_refuel": 50,
      "cost_at_stop": 157.50
    }
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

## Testing with Postman

1. Create a POST request to `http://localhost:8000/api/route/`
2. Set Content-Type header to `application/json`
3. Add request body with start and finish locations
4. Send request and view optimized route with fuel stops


## Quick Test

Run the demo script to test the API:
```bash
python demo_script.py
```

This will test three different routes and display results.

## Project Structure

```
fuel_route_api/
├── fuel_route_api/          # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
├── route_planner/           # Main app
│   ├── services.py          # Route calculation logic
│   ├── fuel_prices.py       # Fuel price data
│   ├── views.py             # API endpoints
│   ├── serializers.py       # Request validation
│   └── urls.py              # App URLs
├── requirements.txt         # Python dependencies
├── manage.py                # Django management
├── setup.py                 # Quick setup script
├── demo_script.py           # API testing script
└── postman_collection.json  # Postman tests
```

## How It Works

1. **Geocoding**: Converts location names to coordinates (2 API calls)
2. **Routing**: Gets route geometry and distance (1 API call)
3. **Fuel Calculation**: 
   - Determines number of stops needed (distance ÷ 500 miles)
   - Interpolates stop positions along route
   - Looks up fuel prices by state
   - Calculates total cost
4. **Response**: Returns route data, fuel stops, and cost summary

Total API calls: 2-3 per request (meets requirement of minimal calls)

## Documentation

- `README.md` - This file
- `QUICK_START.md` - Step-by-step getting started guide
- `IMPLEMENTATION_NOTES.md` - Technical decisions and architecture
- `LOOM_SCRIPT.md` - Script for demo video
- `SUBMISSION_CHECKLIST.md` - Pre-submission verification

## Technologies Used

- Django 5.0.2 (latest stable)
- Django REST Framework 3.14.0
- OpenRouteService API (free tier)
- Python 3.8+
