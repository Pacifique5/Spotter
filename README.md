# Fuel Route Optimizer API

Django REST API that calculates optimal fuel stops along a route based on fuel prices.

## Features
- Route planning between US locations
- Optimal fuel stop recommendations based on price
- Total fuel cost calculation (10 MPG vehicle, 500-mile range)
- Fast response times with minimal external API calls (1-2 API calls total)
- Uses OpenRouteService for routing and geocoding

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a free API key from [OpenRouteService](https://openrouteservice.org/dev/#/signup)

3. Create `.env` file:
```bash
OPENROUTE_API_KEY=your_api_key_here
```

4. Run migrations and start server:
```bash
python manage.py migrate
python manage.py runserver
```

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
