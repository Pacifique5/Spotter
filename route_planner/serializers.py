from rest_framework import serializers


class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(max_length=200, help_text="Starting location (e.g., 'New York, NY')")
    finish = serializers.CharField(max_length=200, help_text="Destination location (e.g., 'Los Angeles, CA')")
    
    def validate_start(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Start location cannot be empty")
        return value.strip()
    
    def validate_finish(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Finish location cannot be empty")
        return value.strip()
