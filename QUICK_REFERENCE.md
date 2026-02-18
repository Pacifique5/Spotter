# Quick Reference Card

## Setup (One-Time)
```bash
# 1. Install
pip install -r requirements.txt

# 2. Get API key from https://openrouteservice.org/dev/#/signup

# 3. Create .env file
echo OPENROUTE_API_KEY=your_key_here > .env

# 4. Initialize
python manage.py migrate
```

## Run Server
```bash
python manage.py runserver
```
Server: http://localhost:8000

## Test API

### Using curl
```bash
curl -X POST http://localhost:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d '{"start": "New York, NY", "finish": "Los Angeles, CA"}'
```

### Using Python
```python
import requests
r = requests.post('http://localhost:8000/api/route/',
    json={'start': 'New York, NY', 'finish': 'Los Angeles, CA'})
print(r.json())
```

### Using Demo Script
```bash
python demo_script.py
```

### Using Postman
Import `postman_collection.json`

## API Endpoint

**POST** `/api/route/`

**Request:**
```json
{"start": "City, State", "finish": "City, State"}
```

**Response:**
```json
{
  "start": {...},
  "finish": {...},
  "route": {"geometry": {...}, "duration_seconds": 142560},
  "fuel_stops": [{...}],
  "summary": {
    "total_distance_miles": 2789.45,
    "total_fuel_gallons": 278.95,
    "total_fuel_cost_usd": 856.32
  }
}
```

## Common Commands

```bash
# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# Run demo
python demo_script.py
```

## File Locations

- **Settings**: `fuel_route_api/settings.py`
- **Main Logic**: `route_planner/services.py`
- **API View**: `route_planner/views.py`
- **Fuel Prices**: `route_planner/fuel_prices.py`
- **Tests**: `route_planner/tests.py`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Location not found" | Use format "City, ST" (e.g., "New York, NY") |
| "External API error" | Check API key in .env file |
| Server won't start | Check port 8000 is available |
| Import errors | Run `pip install -r requirements.txt` |

## Documentation Files

- `README.md` - Main documentation
- `QUICK_START.md` - Getting started
- `DEVELOPER_GUIDE.md` - Technical details
- `PROJECT_SUMMARY.md` - Overview
- `SUBMISSION_CHECKLIST.md` - Pre-submission tasks
- `LOOM_SCRIPT.md` - Video script

## Key Features

✅ Django 5.0.2 (latest stable)
✅ 2-3 API calls per request
✅ Sub-3-second responses
✅ State-based fuel pricing
✅ 500-mile range, 10 MPG
✅ Complete documentation

## Support

Check documentation files for detailed information on:
- Setup and installation
- API usage and examples
- Architecture and algorithms
- Testing and deployment
- Troubleshooting
