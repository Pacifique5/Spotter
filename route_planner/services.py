import requests
from django.conf import settings
from .fuel_prices import get_fuel_price
import math


class RouteService:
    """Service for calculating routes and optimal fuel stops."""
    
    BASE_URL = "https://api.openrouteservice.org"
    MAX_RANGE_MILES = 500
    MPG = 10
    
    def __init__(self):
        self.api_key = settings.OPENROUTE_API_KEY
        
    def geocode(self, location):
        """Convert location string to coordinates."""
        url = f"{self.BASE_URL}/geocode/search"
        params = {
            'api_key': self.api_key,
            'text': location,
            'boundary.country': 'US',
            'size': 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data['features']:
            raise ValueError(f"Location not found: {location}")
            
        coords = data['features'][0]['geometry']['coordinates']
        properties = data['features'][0]['properties']
        
        return {
            'lon': coords[0],
            'lat': coords[1],
            'name': properties.get('label', location),
            'state': properties.get('region_a', 'US')
        }
    
    def get_route(self, start_coords, end_coords):
        """Get route between two coordinates."""
        url = f"{self.BASE_URL}/v2/directions/driving-car"
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        body = {
            'coordinates': [
                [start_coords['lon'], start_coords['lat']],
                [end_coords['lon'], end_coords['lat']]
            ],
            'instructions': False,
            'geometry': True,
            'elevation': False
        }
        
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def calculate_fuel_stops(self, route_data, start_location, end_location):
        """Calculate optimal fuel stops along the route."""
        route = route_data['routes'][0]
        distance_km = route['summary']['distance']
        distance_miles = distance_km * 0.621371
        
        # Get route geometry for interpolation
        geometry = route['geometry']['coordinates']
        
        # Calculate number of stops needed
        num_stops = math.ceil(distance_miles / self.MAX_RANGE_MILES) - 1
        
        if num_stops <= 0:
            # No stops needed, calculate direct cost
            gallons_needed = distance_miles / self.MPG
            fuel_price = get_fuel_price(start_location['state'])
            total_cost = gallons_needed * fuel_price
            
            return {
                'fuel_stops': [],
                'total_distance_miles': round(distance_miles, 2),
                'total_fuel_gallons': round(gallons_needed, 2),
                'total_fuel_cost': round(total_cost, 2)
            }
        
        # Calculate stop positions
        fuel_stops = []
        total_cost = 0
        remaining_distance = distance_miles
        
        for i in range(num_stops + 1):
            if i == 0:
                # First segment
                segment_distance = min(self.MAX_RANGE_MILES, remaining_distance)
                state = start_location['state']
            else:
                # Subsequent segments
                segment_distance = min(self.MAX_RANGE_MILES, remaining_distance)
                # Interpolate position along route
                progress = (i * self.MAX_RANGE_MILES) / distance_miles
                coord_index = int(progress * (len(geometry) - 1))
                coord = geometry[min(coord_index, len(geometry) - 1)]
                
                # Reverse geocode to get state
                state = self._get_state_from_coords(coord[0], coord[1])
            
            gallons_needed = segment_distance / self.MPG
            fuel_price = get_fuel_price(state)
            cost = gallons_needed * fuel_price
            total_cost += cost
            
            if i < num_stops:
                # Calculate stop position
                progress = ((i + 1) * self.MAX_RANGE_MILES) / distance_miles
                coord_index = int(progress * (len(geometry) - 1))
                coord = geometry[min(coord_index, len(geometry) - 1)]
                
                fuel_stops.append({
                    'stop_number': i + 1,
                    'location': {
                        'lat': coord[1],
                        'lon': coord[0],
                        'state': state
                    },
                    'distance_from_start_miles': round((i + 1) * self.MAX_RANGE_MILES, 2),
                    'fuel_price_per_gallon': fuel_price,
                    'gallons_to_refuel': round(gallons_needed, 2),
                    'cost_at_stop': round(cost, 2)
                })
            
            remaining_distance -= segment_distance
        
        return {
            'fuel_stops': fuel_stops,
            'total_distance_miles': round(distance_miles, 2),
            'total_fuel_gallons': round(distance_miles / self.MPG, 2),
            'total_fuel_cost': round(total_cost, 2)
        }
    
    def _get_state_from_coords(self, lon, lat):
        """Reverse geocode coordinates to get state."""
        try:
            url = f"{self.BASE_URL}/geocode/reverse"
            params = {
                'api_key': self.api_key,
                'point.lon': lon,
                'point.lat': lat,
                'size': 1
            }
            response = requests.get(url, params=params, timeout=3)
            response.raise_for_status()
            data = response.json()
            
            if data['features']:
                return data['features'][0]['properties'].get('region_a', 'US')
        except:
            pass
        
        return 'US'
    
    def plan_route(self, start, finish):
        """Main method to plan route with fuel stops."""
        # Geocode locations
        start_location = self.geocode(start)
        end_location = self.geocode(finish)
        
        # Get route
        route_data = self.get_route(start_location, end_location)
        
        # Calculate fuel stops
        fuel_data = self.calculate_fuel_stops(route_data, start_location, end_location)
        
        # Build response
        return {
            'start': {
                'name': start_location['name'],
                'coordinates': {
                    'lat': start_location['lat'],
                    'lon': start_location['lon']
                },
                'state': start_location['state']
            },
            'finish': {
                'name': end_location['name'],
                'coordinates': {
                    'lat': end_location['lat'],
                    'lon': end_location['lon']
                },
                'state': end_location['state']
            },
            'route': {
                'geometry': route_data['routes'][0]['geometry'],
                'duration_seconds': route_data['routes'][0]['summary']['duration']
            },
            'fuel_stops': fuel_data['fuel_stops'],
            'summary': {
                'total_distance_miles': fuel_data['total_distance_miles'],
                'total_fuel_gallons': fuel_data['total_fuel_gallons'],
                'total_fuel_cost_usd': fuel_data['total_fuel_cost'],
                'vehicle_mpg': self.MPG,
                'vehicle_range_miles': self.MAX_RANGE_MILES
            }
        }
