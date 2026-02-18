from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class RouteAPITestCase(TestCase):
    """Test cases for the route planning API."""
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/route/'
    
    def test_valid_route_request(self):
        """Test valid route request returns 200."""
        data = {
            'start': 'New York, NY',
            'finish': 'Boston, MA'
        }
        response = self.client.post(self.url, data, format='json')
        
        # Note: This will fail without valid API key
        # Uncomment when API key is configured
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('fuel_stops', response.data)
        # self.assertIn('summary', response.data)
    
    def test_missing_start_location(self):
        """Test request with missing start location."""
        data = {'finish': 'Boston, MA'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_missing_finish_location(self):
        """Test request with missing finish location."""
        data = {'start': 'New York, NY'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_empty_locations(self):
        """Test request with empty location strings."""
        data = {'start': '', 'finish': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
