# Setup Guide

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation Steps

### 1. Clone or Download the Project
```bash
cd fuel-route-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:
```
OPENROUTE_API_KEY=your_api_key_here
```

Get your free API key from: https://openrouteservice.org/dev/#/signup

### 6. Run Database Migrations
```bash
python manage.py migrate
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## API Usage

### Endpoint
```
POST http://localhost:8000/api/route/
```

### Request Body
```json
{
    "start": "New York, NY",
    "finish": "Los Angeles, CA"
}
```

### Example with cURL
```bash
curl -X POST http://localhost:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d "{\"start\": \"New York, NY\", \"finish\": \"Los Angeles, CA\"}"
```

### Example with Python
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

## How It Works

1. **Geocoding**: Converts location names to coordinates using OpenRouteService
2. **Route Calculation**: Gets the optimal driving route between locations
3. **Fuel Price Data**: Loads real fuel prices from `fuel-prices-for-be-assessment.csv` (8000+ truck stops)
4. **Fuel Stop Planning**: Calculates optimal refueling stops based on:
   - Vehicle range: 500 miles
   - Fuel efficiency: 10 MPG
   - State-averaged fuel prices from CSV data
5. **Cost Calculation**: Computes total fuel cost for the journey

## Response Structure

The API returns:
- Start and finish location details with coordinates
- Route geometry for mapping
- List of fuel stops with:
  - Location coordinates
  - Distance from start
  - Fuel price per gallon
  - Gallons needed
  - Cost at each stop
- Summary with total distance, fuel needed, and total cost

## Troubleshooting

**API Key Error**: Make sure your `.env` file contains a valid OpenRouteService API key

**Location Not Found**: Use clear location names like "City, State" format

**CSV File Missing**: Ensure `fuel-prices-for-be-assessment.csv` is in the project root

## Testing
```bash
python manage.py test
```
