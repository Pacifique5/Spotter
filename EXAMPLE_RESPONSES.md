# Example API Responses

## Example 1: Short Route (No Fuel Stops)

### Request
```json
POST /api/route/
{
  "start": "Boston, MA",
  "finish": "New York, NY"
}
```

### Response
```json
{
  "start": {
    "name": "Boston, Massachusetts, United States",
    "coordinates": {
      "lat": 42.3601,
      "lon": -71.0589
    },
    "state": "MA"
  },
  "finish": {
    "name": "New York, New York, United States",
    "coordinates": {
      "lat": 40.7128,
      "lon": -74.0060
    },
    "state": "NY"
  },
  "route": {
    "geometry": {
      "coordinates": [
        [-71.0589, 42.3601],
        [-71.0612, 42.3589],
        ...
        [-74.0060, 40.7128]
      ],
      "type": "LineString"
    },
    "duration_seconds": 14520
  },
  "fuel_stops": [],
  "summary": {
    "total_distance_miles": 215.3,
    "total_fuel_gallons": 21.53,
    "total_fuel_cost_usd": 72.12,
    "vehicle_mpg": 10,
    "vehicle_range_miles": 500
  }
}
```

**Analysis:**
- Distance: 215 miles (under 500-mile range)
- No fuel stops needed
- Total cost: $72.12 (based on MA fuel price of $3.35/gallon)
- Trip duration: ~4 hours

---

## Example 2: Medium Route (1 Fuel Stop)

### Request
```json
POST /api/route/
{
  "start": "New York, NY",
  "finish": "Chicago, IL"
}
```

### Response
```json
{
  "start": {
    "name": "New York, New York, United States",
    "coordinates": {
      "lat": 40.7128,
      "lon": -74.0060
    },
    "state": "NY"
  },
  "finish": {
    "name": "Chicago, Illinois, United States",
    "coordinates": {
      "lat": 41.8781,
      "lon": -87.6298
    },
    "state": "IL"
  },
  "route": {
    "geometry": {
      "coordinates": [
        [-74.0060, 40.7128],
        [-74.0089, 40.7115],
        ...
        [-87.6298, 41.8781]
      ],
      "type": "LineString"
    },
    "duration_seconds": 45360
  },
  "fuel_stops": [
    {
      "stop_number": 1,
      "location": {
        "lat": 40.4406,
        "lon": -79.9959,
        "state": "PA"
      },
      "distance_from_start_miles": 500.0,
      "fuel_price_per_gallon": 3.58,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 179.00
    }
  ],
  "summary": {
    "total_distance_miles": 789.5,
    "total_fuel_gallons": 78.95,
    "total_fuel_cost_usd": 282.68,
    "vehicle_mpg": 10,
    "vehicle_range_miles": 500
  }
}
```

**Analysis:**
- Distance: 789 miles
- 1 fuel stop in Pennsylvania (after 500 miles)
- Stop location: Pittsburgh area
- Total cost: $282.68
- Trip duration: ~12.6 hours

---

## Example 3: Long Route (5 Fuel Stops)

### Request
```json
POST /api/route/
{
  "start": "New York, NY",
  "finish": "Los Angeles, CA"
}
```

### Response
```json
{
  "start": {
    "name": "New York, New York, United States",
    "coordinates": {
      "lat": 40.7128,
      "lon": -74.0060
    },
    "state": "NY"
  },
  "finish": {
    "name": "Los Angeles, California, United States",
    "coordinates": {
      "lat": 34.0522,
      "lon": -118.2437
    },
    "state": "CA"
  },
  "route": {
    "geometry": {
      "coordinates": [
        [-74.0060, 40.7128],
        ...
        [-118.2437, 34.0522]
      ],
      "type": "LineString"
    },
    "duration_seconds": 142560
  },
  "fuel_stops": [
    {
      "stop_number": 1,
      "location": {
        "lat": 39.9612,
        "lon": -82.9988,
        "state": "OH"
      },
      "distance_from_start_miles": 500.0,
      "fuel_price_per_gallon": 3.15,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 157.50
    },
    {
      "stop_number": 2,
      "location": {
        "lat": 39.7684,
        "lon": -89.6540,
        "state": "IL"
      },
      "distance_from_start_miles": 1000.0,
      "fuel_price_per_gallon": 3.42,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 171.00
    },
    {
      "stop_number": 3,
      "location": {
        "lat": 38.5767,
        "lon": -92.1735,
        "state": "MO"
      },
      "distance_from_start_miles": 1500.0,
      "fuel_price_per_gallon": 2.85,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 142.50
    },
    {
      "stop_number": 4,
      "location": {
        "lat": 35.4676,
        "lon": -97.5164,
        "state": "OK"
      },
      "distance_from_start_miles": 2000.0,
      "fuel_price_per_gallon": 2.82,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 141.00
    },
    {
      "stop_number": 5,
      "location": {
        "lat": 35.0844,
        "lon": -106.6504,
        "state": "NM"
      },
      "distance_from_start_miles": 2500.0,
      "fuel_price_per_gallon": 2.95,
      "gallons_to_refuel": 50.0,
      "cost_at_stop": 147.50
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

**Analysis:**
- Distance: 2,789 miles
- 5 fuel stops across OH, IL, MO, OK, NM
- Cheapest fuel: Oklahoma ($2.82/gal)
- Most expensive: Illinois ($3.42/gal)
- Total cost: $856.32
- Trip duration: ~39.6 hours

---

## Example 4: Error Response - Invalid Location

### Request
```json
POST /api/route/
{
  "start": "InvalidCity, XX",
  "finish": "Los Angeles, CA"
}
```

### Response (404 Not Found)
```json
{
  "error": "Location not found: InvalidCity, XX"
}
```

---

## Example 5: Error Response - Missing Parameters

### Request
```json
POST /api/route/
{
  "start": "New York, NY"
}
```

### Response (400 Bad Request)
```json
{
  "error": "Invalid input",
  "details": {
    "finish": [
      "This field is required."
    ]
  }
}
```

---

## Example 6: Error Response - Empty Values

### Request
```json
POST /api/route/
{
  "start": "",
  "finish": "Los Angeles, CA"
}
```

### Response (400 Bad Request)
```json
{
  "error": "Invalid input",
  "details": {
    "start": [
      "Start location cannot be empty"
    ]
  }
}
```

---

## Response Field Descriptions

### Start/Finish Objects
- `name`: Full location name from geocoding service
- `coordinates.lat`: Latitude in decimal degrees
- `coordinates.lon`: Longitude in decimal degrees
- `state`: Two-letter state code

### Route Object
- `geometry`: GeoJSON LineString with route coordinates
- `duration_seconds`: Estimated travel time in seconds

### Fuel Stop Objects
- `stop_number`: Sequential stop number (1, 2, 3, ...)
- `location.lat/lon`: Stop coordinates
- `location.state`: State where stop is located
- `distance_from_start_miles`: Cumulative distance from start
- `fuel_price_per_gallon`: Price at this location
- `gallons_to_refuel`: Amount needed for next segment
- `cost_at_stop`: Cost for this refueling

### Summary Object
- `total_distance_miles`: Total route distance
- `total_fuel_gallons`: Total fuel needed for entire trip
- `total_fuel_cost_usd`: Total cost for all fuel
- `vehicle_mpg`: Vehicle fuel efficiency (constant: 10)
- `vehicle_range_miles`: Vehicle range (constant: 500)

---

## Using the Geometry Data

The `route.geometry` field contains GeoJSON LineString data that can be used with mapping libraries:

### Leaflet.js Example
```javascript
const routeData = response.route.geometry;
const routeLine = L.geoJSON(routeData, {
  style: { color: 'blue', weight: 3 }
}).addTo(map);

// Add fuel stop markers
response.fuel_stops.forEach(stop => {
  L.marker([stop.location.lat, stop.location.lon])
    .bindPopup(`Stop ${stop.stop_number}: $${stop.cost_at_stop}`)
    .addTo(map);
});
```

### Google Maps Example
```javascript
const path = response.route.geometry.coordinates.map(coord => ({
  lat: coord[1],
  lng: coord[0]
}));

const routePath = new google.maps.Polyline({
  path: path,
  geodesic: true,
  strokeColor: '#0000FF',
  strokeWeight: 3
});
routePath.setMap(map);
```
