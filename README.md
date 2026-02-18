# Fuel Route Optimizer API

Django REST API that calculates optimal fuel stops for long-distance routes in the USA using real fuel price data from 8,151 truck stops.

## Features

- Route planning between any two US locations
- Optimal fuel stop recommendations based on real fuel prices
- Total fuel cost calculation (10 MPG vehicle, 500-mile range)
- Complete route geometry for map visualization
- Fast response times with minimal external API calls

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your OpenRouteService API key
echo OPENROUTE_API_KEY=your_api_key_here > .env

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

Server runs at: **http://127.0.0.1:8000**

## API Usage

**Endpoint:** POST `/api/route/`

**Request:**
```json
{
  "start": "New York, NY",
  "finish": "Los Angeles, CA"
}
```

**Response:**
```json
{
  "start": { "name": "New York, NY, USA", "coordinates": {...}, "state": "NY" },
  "finish": { "name": "Los Angeles, CA, USA", "coordinates": {...}, "state": "CA" },
  "route": { "geometry": {...}, "duration_seconds": 142560 },
  "fuel_stops": [
    {
      "stop_number": 1,
      "distance_from_start_miles": 500.0,
      "state": "OH",
      "fuel_price_per_gallon": 3.15,
      "gallons_to_refuel": 50.0,
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

### Using cURL
```bash
curl -X POST http://127.0.0.1:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d '{"start": "New York, NY", "finish": "Boston, MA"}'
```

### Using Postman
Import `postman_collection.json` for pre-configured test requests.

### Using Python
```python
import requests

response = requests.post('http://127.0.0.1:8000/api/route/', json={
    'start': 'New York, NY',
    'finish': 'Los Angeles, CA'
})

print(response.json())
```

## How It Works

1. **Geocoding**: Converts location names to coordinates (OpenRouteService API)
2. **Routing**: Gets optimal driving route with distance and geometry
3. **Fuel Calculation**: 
   - Loads real prices from `fuel-prices-for-be-assessment.csv` (8,151 truck stops)
   - Calculates state-averaged fuel prices
   - Determines stops every 500 miles (vehicle range)
   - Computes total cost using 10 MPG efficiency
4. **Response**: Returns complete route with fuel stops and costs

## Technology Stack

- **Django** 5.0.2 + Django REST Framework 3.14.0
- **OpenRouteService API** (free tier) for geocoding and routing
- **Python** 3.8+
- **Real Fuel Data** from CSV (8,151 truck stops across USA)

## Project Structure

```
fuel_route_api/
├── fuel_route_api/          # Django project settings
├── route_planner/           # Main application
│   ├── views.py             # API endpoint
│   ├── services.py          # Route calculation logic
│   ├── fuel_prices.py       # CSV data loader
│   └── serializers.py       # Request validation
├── fuel-prices-for-be-assessment.csv  # Real fuel price data
├── .env                     # API key configuration
├── requirements.txt         # Python dependencies
├── manage.py                # Django CLI
├── postman_collection.json  # API test collection
├── README.md                # This file
└── SETUP.md                 # Detailed setup guide
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup instructions with all commands and troubleshooting

## Requirements Met

✓ Django 5.0.2 (latest stable)  
✓ US location input (start/finish)  
✓ Route map with geometry  
✓ Optimal fuel stops by cost  
✓ 500-mile vehicle range  
✓ 10 MPG fuel efficiency  
✓ Real CSV data (8,151 truck stops)  
✓ Free routing API (OpenRouteService)  
✓ Minimal API calls (2-3 per request)  
✓ Fast response times  

## Get OpenRouteService API Key

1. Sign up at: https://openrouteservice.org/dev/#/signup
2. Copy your API key
3. Add to `.env` file: `OPENROUTE_API_KEY=your_key_here`

## License

This project was created as an assignment demonstration.
