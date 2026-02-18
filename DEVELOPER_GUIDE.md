# Developer Guide

## Overview

This Django API calculates optimal fuel stops for road trips across the USA. It uses OpenRouteService for routing and state-based fuel pricing to minimize costs.

## Architecture

### Components

1. **RouteService** (`services.py`)
   - Core business logic
   - Handles geocoding, routing, and fuel calculations
   - Manages external API calls

2. **API Views** (`views.py`)
   - REST endpoint implementation
   - Request validation
   - Error handling

3. **Fuel Pricing** (`fuel_prices.py`)
   - State-by-state fuel prices
   - Fast in-memory lookup

4. **Serializers** (`serializers.py`)
   - Input validation
   - Data transformation

### Data Flow

```
Client Request
    ↓
RouteView (validation)
    ↓
RouteService.plan_route()
    ↓
├─→ geocode(start) ────→ OpenRouteService API
├─→ geocode(finish) ───→ OpenRouteService API
├─→ get_route() ───────→ OpenRouteService API
└─→ calculate_fuel_stops()
    ├─→ Interpolate positions
    ├─→ Lookup fuel prices
    └─→ Calculate costs
    ↓
JSON Response
```

## Key Algorithms

### Fuel Stop Calculation

```python
# Pseudocode
total_distance = route_distance_in_miles
num_stops = ceil(total_distance / 500) - 1

for each segment:
    segment_distance = min(500, remaining_distance)
    position = interpolate_along_route(segment_index)
    state = get_state_at_position(position)
    fuel_price = lookup_price(state)
    gallons = segment_distance / 10  # 10 MPG
    cost = gallons * fuel_price
    
    if not last_segment:
        add_fuel_stop(position, cost, gallons)
```

### Route Interpolation

Instead of making multiple routing API calls, we:
1. Get full route geometry once
2. Calculate stop positions mathematically
3. Interpolate coordinates from geometry array

This reduces API calls from O(n) to O(1) where n = number of stops.

## Performance Optimizations

### 1. Minimal API Calls
- Only 2-3 external API calls per request
- Geocoding: 2 calls (start/finish)
- Routing: 1 call
- Reverse geocoding: Optional, with fallback

### 2. In-Memory Data
- Fuel prices stored in Python dict
- O(1) lookup time
- No database overhead

### 3. Efficient Calculations
- Single-pass fuel stop calculation
- No recursive or nested API calls
- Linear time complexity O(n) where n = number of stops

### 4. Stateless Design
- No database queries
- No session management
- Horizontally scalable

## API Reference

### POST /api/route/

Calculate optimal route with fuel stops.

**Request:**
```json
{
  "start": "string (required)",
  "finish": "string (required)"
}
```

**Response (200 OK):**
```json
{
  "start": {
    "name": "string",
    "coordinates": {"lat": float, "lon": float},
    "state": "string"
  },
  "finish": {
    "name": "string",
    "coordinates": {"lat": float, "lon": float},
    "state": "string"
  },
  "route": {
    "geometry": {...},
    "duration_seconds": int
  },
  "fuel_stops": [
    {
      "stop_number": int,
      "location": {"lat": float, "lon": float, "state": "string"},
      "distance_from_start_miles": float,
      "fuel_price_per_gallon": float,
      "gallons_to_refuel": float,
      "cost_at_stop": float
    }
  ],
  "summary": {
    "total_distance_miles": float,
    "total_fuel_gallons": float,
    "total_fuel_cost_usd": float,
    "vehicle_mpg": int,
    "vehicle_range_miles": int
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input
- `404 Not Found`: Location not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: External API error

## Configuration

### Environment Variables

- `OPENROUTE_API_KEY`: Required. Get from https://openrouteservice.org
- `DEBUG`: Optional. Set to False in production
- `SECRET_KEY`: Change in production

### Constants (in services.py)

```python
MAX_RANGE_MILES = 500  # Vehicle range
MPG = 10               # Fuel efficiency
```

Modify these to test different vehicle types.

## Testing

### Unit Tests
```bash
python manage.py test
```

### Integration Test
```bash
python demo_script.py
```

### Manual Testing
Use Postman collection: `postman_collection.json`

## Extending the API

### Add New Vehicle Types

1. Modify `RouteService.__init__()` to accept parameters:
```python
def __init__(self, mpg=10, range_miles=500):
    self.MPG = mpg
    self.MAX_RANGE_MILES = range_miles
```

2. Update view to accept query parameters:
```python
mpg = request.query_params.get('mpg', 10)
range_miles = request.query_params.get('range', 500)
```

### Add Real-Time Fuel Prices

1. Create new service: `fuel_price_api.py`
2. Implement API client for fuel price service
3. Add caching to reduce API calls
4. Update `get_fuel_price()` to use API

### Add Route Alternatives

1. Modify `get_route()` to request alternatives:
```python
body = {
    'coordinates': [...],
    'alternative_routes': {'target_count': 3}
}
```

2. Return multiple route options with costs
3. Let client choose preferred route

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL)
- [ ] Set up HTTPS
- [ ] Configure CORS if needed
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Use environment variables for secrets

### Deployment Options

1. **Heroku**: Easy deployment with Procfile
2. **AWS Elastic Beanstalk**: Scalable Django hosting
3. **DigitalOcean App Platform**: Simple deployment
4. **Docker**: Containerized deployment

## Troubleshooting

### "Location not found"
- Use format: "City, State" (e.g., "New York, NY")
- Ensure location is in USA
- Check spelling

### "External API error"
- Verify API key in .env file
- Check OpenRouteService status
- Verify internet connection
- Check API rate limits (2000/day free tier)

### Slow responses
- Check network latency
- Verify API key is valid
- Consider caching geocoding results
- Check OpenRouteService server status

### Import errors
- Run `pip install -r requirements.txt`
- Verify Python version (3.8+)
- Check virtual environment is activated

## Support

For issues or questions:
1. Check documentation files
2. Review error messages
3. Test with demo_script.py
4. Verify API key configuration
