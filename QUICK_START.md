# Quick Start Guide

## Installation (5 minutes)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Get your free API key:
   - Visit https://openrouteservice.org/dev/#/signup
   - Sign up (takes 1 minute)
   - Copy your API key

3. Create `.env` file in project root:
```bash
OPENROUTE_API_KEY=your_actual_api_key_here
```

4. Initialize Django:
```bash
python manage.py migrate
```

5. Start the server:
```bash
python manage.py runserver
```

Server will be running at `http://localhost:8000`

## Test the API

### Using curl:

```bash
curl -X POST http://localhost:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d "{\"start\": \"New York, NY\", \"finish\": \"Chicago, IL\"}"
```

### Using Postman:
1. Import `postman_collection.json`
2. Select "Calculate Route with Fuel Stops"
3. Click Send

### Using Python:
```python
import requests

response = requests.post(
    'http://localhost:8000/api/route/',
    json={
        'start': 'New York, NY',
        'finish': 'Los Angeles, CA'
    }
)

print(response.json())
```

## Example Routes to Test

1. Short route (no fuel stops needed):
   - Start: "Boston, MA"
   - Finish: "New York, NY"

2. Medium route (1-2 stops):
   - Start: "New York, NY"
   - Finish: "Chicago, IL"

3. Long route (5+ stops):
   - Start: "New York, NY"
   - Finish: "Los Angeles, CA"

4. Cross-country:
   - Start: "Miami, FL"
   - Finish: "Seattle, WA"

## Response Structure

The API returns:
- Start/finish location details with coordinates
- Route geometry (for map visualization)
- List of optimal fuel stops with:
  - Location coordinates and state
  - Distance from start
  - Fuel price at that location
  - Gallons needed
  - Cost at that stop
- Summary with total distance, fuel, and cost

## Troubleshooting

- "Location not found": Use format "City, State" (e.g., "New York, NY")
- "External API error": Check your API key in `.env` file
- Server won't start: Make sure port 8000 is available
