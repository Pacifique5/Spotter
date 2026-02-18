# API Flow Diagram

## Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                          │
│  POST /api/route/                                              │
│  {"start": "New York, NY", "finish": "Los Angeles, CA"}       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO REST FRAMEWORK                      │
│  RouteView.post()                                              │
│  • Validates input (RouteRequestSerializer)                    │
│  • Handles errors                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ROUTE SERVICE                             │
│  RouteService.plan_route()                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   GEOCODE START          │  │   GEOCODE FINISH         │
│   API Call #1            │  │   API Call #2            │
│   ↓                      │  │   ↓                      │
│   Returns:               │  │   Returns:               │
│   • Coordinates          │  │   • Coordinates          │
│   • State                │  │   • State                │
└──────────┬───────────────┘  └──────────┬───────────────┘
           │                             │
           └──────────────┬──────────────┘
                          ▼
           ┌──────────────────────────────┐
           │      GET ROUTE               │
           │      API Call #3             │
           │      ↓                       │
           │      Returns:                │
           │      • Route geometry        │
           │      • Total distance        │
           │      • Duration              │
           └──────────────┬───────────────┘
                          ▼
           ┌──────────────────────────────┐
           │  CALCULATE FUEL STOPS        │
           │  (No API calls)              │
           │                              │
           │  1. Calculate # of stops     │
           │     stops = distance/500     │
           │                              │
           │  2. For each stop:           │
           │     • Interpolate position   │
           │       from route geometry    │
           │     • Determine state        │
           │     • Lookup fuel price      │
           │     • Calculate cost         │
           │                              │
           │  3. Sum total costs          │
           └──────────────┬───────────────┘
                          ▼
           ┌──────────────────────────────┐
           │     BUILD RESPONSE           │
           │                              │
           │  • Start/finish details      │
           │  • Route geometry            │
           │  • Fuel stops array          │
           │  • Cost summary              │
           └──────────────┬───────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         JSON RESPONSE                           │
│  {                                                              │
│    "start": {...},                                             │
│    "finish": {...},                                            │
│    "route": {"geometry": {...}},                              │
│    "fuel_stops": [{...}, {...}, ...],                         │
│    "summary": {                                                │
│      "total_distance_miles": 2789.45,                         │
│      "total_fuel_cost_usd": 856.32                            │
│    }                                                           │
│  }                                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Details

### Phase 1: Geocoding (2 API calls)
```
Input: "New York, NY"
  ↓
OpenRouteService Geocoding API
  ↓
Output: {lat: 40.7128, lon: -74.0060, state: "NY"}
```

### Phase 2: Routing (1 API call)
```
Input: Start coords + End coords
  ↓
OpenRouteService Directions API
  ↓
Output: {
  distance: 4489 km,
  geometry: [[lon, lat], [lon, lat], ...],
  duration: 142560 seconds
}
```

### Phase 3: Fuel Calculation (0 API calls)
```
Input: Route geometry + distance
  ↓
Calculate stops needed: ceil(2789 miles / 500) - 1 = 5 stops
  ↓
For each stop:
  position = (stop_number * 500) / total_distance
  coords = geometry[position * geometry.length]
  state = reverse_geocode(coords) or fallback
  price = FUEL_PRICES[state]
  gallons = 500 / 10 = 50
  cost = gallons * price
  ↓
Sum all costs
```

## Performance Characteristics

| Operation | Time Complexity | API Calls |
|-----------|----------------|-----------|
| Geocoding | O(1) | 2 |
| Routing | O(1) | 1 |
| Fuel calculation | O(n) | 0 |
| Price lookup | O(1) | 0 |
| **Total** | **O(n)** | **2-3** |

Where n = number of fuel stops (typically 0-7)

## Comparison with Naive Approach

### Naive Approach (Multiple Routing Calls)
```
Geocode start → 1 call
Geocode finish → 1 call
Route to stop 1 → 1 call
Route to stop 2 → 1 call
Route to stop 3 → 1 call
...
Total: 3 + n calls (8-10 for cross-country)
Response time: 5-10 seconds
```

### Our Approach (Geometry Interpolation)
```
Geocode start → 1 call
Geocode finish → 1 call
Route with geometry → 1 call
Interpolate all stops → 0 calls
Total: 3 calls (regardless of distance)
Response time: 1-3 seconds
```

## Error Handling Flow

```
Request
  ↓
Validation Error? → 400 Bad Request
  ↓
Location Not Found? → 404 Not Found
  ↓
API Error? → 503 Service Unavailable
  ↓
Server Error? → 500 Internal Server Error
  ↓
Success → 200 OK
```

## Caching Opportunities (Future Enhancement)

```
┌─────────────────┐
│  Request        │
└────────┬────────┘
         ▼
    ┌────────────┐
    │ Cache Hit? │
    └─┬────────┬─┘
      │        │
     Yes       No
      │        │
      ▼        ▼
   Return   Call API
   Cached    & Cache
   Result    Result
```

Potential cache keys:
- Geocoding: `geocode:{location_string}`
- Routes: `route:{start_coords}:{end_coords}`
- TTL: 24 hours for geocoding, 1 hour for routes
