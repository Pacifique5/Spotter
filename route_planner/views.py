from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import RouteRequestSerializer
from .services import RouteService


class RouteView(APIView):
    """
    API endpoint for route planning with optimal fuel stops.
    
    POST /api/route/
    {
        "start": "New York, NY",
        "finish": "Los Angeles, CA"
    }
    """
    
    def post(self, request):
        serializer = RouteRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid input', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            route_service = RouteService()
            result = route_service.plan_route(
                serializer.validated_data['start'],
                serializer.validated_data['finish']
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': 'External API error', 'details': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
