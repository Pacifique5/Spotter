# Fuel Route Optimizer API

Django REST API that calculates optimal fuel stops along a route using real fuel price data from 8000+ truck stops across the US.

## Features
- Route planning between US locations
- Optimal fuel stop recommendations based on real fuel prices
- Total fuel cost calculation (10 MPG vehicle, 500-mile range)
- Uses real fuel price data from CSV (8000+ truck stops)
- OpenRouteService integration for routing and geocoding

## Quick Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get API key** from [OpenRouteService](https://openrouteservice.org/dev/#/signup)

3. **Create `.env` file:**
```
OPENROUTE_API_KEY=your_api_key_here
```

4. **Run migrations and start server:**
```bash
python manage.py migrate
python manage.py runserver
```

Server runs at `http://localhost:8000`

For detailed setup instructions, see [SETUP.md](SETUP.md)

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

## Testing

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d "{\"start\": \"New York, NY\", \"finish\": \"Los Angeles, CA\"}"
```

**Using Postman:**
Import `postman_collection.json` for pre-configured test requests.

## Project Structure

```
fuel_route_api/
├── fuel_route_api/          # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI config
├── route_planner/           # Main application
│   ├── services.py          # Route calculation logic
│   ├── fuel_prices.py       # CSV data loader & fuel prices
│   ├── views.py             # API endpoints
│   ├── serializers.py       # Request validation
│   └── urls.py              # App URLs
├── fuel-prices-for-be-assessment.csv  # Real fuel price data (8000+ stops)
├── requirements.txt         # Python dependencies
├── manage.py                # Django CLI
├── postman_collection.json  # API test collection
├── README.md                # Project overview
└── SETUP.md                 # Detailed setup guide
```

## How It Works

1. **Load Fuel Data**: Reads `fuel-prices-for-be-assessment.csv` with 8000+ truck stops and calculates state-averaged prices
2. **Geocoding**: Converts location names to coordinates using OpenRouteService
3. **Routing**: Gets optimal driving route with geometry and distance
4. **Fuel Stop Planning**: 
   - Calculates stops needed based on 500-mile vehicle range
   - Interpolates stop positions along route
   - Applies real fuel prices from CSV data (averaged by state)
   - Computes fuel cost for each segment
5. **Response**: Returns complete route with fuel stops and total cost

## Technologies

- Django 5.0.2 + Django REST Framework 3.14.0
- OpenRouteService API (routing & geocoding)
- Python 3.8+
- Real fuel price data from CSV (8000+ truck stops)
