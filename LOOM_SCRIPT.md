# Loom Video Script (5 minutes)

## Introduction (30 seconds)
"Hi! I'm demonstrating the Fuel Route Optimizer API I built for the Django Developer assignment. This API calculates optimal fuel stops along a route based on fuel prices across different states."

## Quick Overview (30 seconds)
"The API is built with Django 5.0 and Django REST Framework. It uses OpenRouteService for routing - a free API that gives us route geometry and distance. The app calculates where to stop for fuel based on a 500-mile range and 10 MPG vehicle, optimizing for cost."

## Postman Demo (2 minutes)

### Test 1: Short Route
"Let me start with a short route - Boston to New York. This is under 500 miles, so no fuel stops needed."
- Show POST request to `/api/route/`
- Show request body: `{"start": "Boston, MA", "finish": "New York, NY"}`
- Send request
- Point out: distance, fuel cost, empty fuel_stops array

### Test 2: Medium Route
"Now a medium route - New York to Chicago. This needs 1-2 fuel stops."
- Change request body: `{"start": "New York, NY", "finish": "Chicago, IL"}`
- Send request
- Point out: fuel stops with locations, prices per state, cost breakdown

### Test 3: Long Route
"Finally, a cross-country route - New York to Los Angeles."
- Change request body: `{"start": "New York, NY", "finish": "Los Angeles, CA"}`
- Send request
- Point out: multiple stops, total cost, route geometry for mapping

## Code Walkthrough (2 minutes)

### Project Structure
"Let me show you the code structure quickly."
- Show file tree: settings, urls, route_planner app

### Key Files

#### services.py
"The RouteService class handles all the logic:"
- `geocode()` - converts locations to coordinates (2 API calls)
- `get_route()` - gets route from OpenRouteService (1 API call)
- `calculate_fuel_stops()` - interpolates stop positions along route geometry
- "Total: 3 API calls maximum, usually 2-3 depending on reverse geocoding"

#### fuel_prices.py
"Fuel prices are stored in-memory as a Python dict - instant lookup, no database needed."

#### views.py
"Simple REST API view with error handling for invalid locations and API failures."

### Performance Features
"Key optimizations:"
- Only 2-3 external API calls total
- No database queries - stateless service
- Route geometry interpolation instead of multiple routing calls
- Fast response times (typically under 2 seconds)

## Wrap Up (30 seconds)
"The API meets all requirements:"
- ✓ Django 5.0
- ✓ Takes start/finish locations
- ✓ Returns route map geometry
- ✓ Calculates optimal fuel stops
- ✓ 500-mile range, 10 MPG
- ✓ Total fuel cost
- ✓ Fast responses with minimal API calls

"Thanks for watching! The code is ready to review."

---

## Tips for Recording
- Have server running before starting
- Have Postman collection imported
- Keep browser tabs ready: code editor, Postman
- Speak clearly and at moderate pace
- Show enthusiasm but stay professional
- Keep it under 5 minutes!
