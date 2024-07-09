from rest_framework import serializers

class APIExceptionSerializer(serializers.Serializer):
    """
    Serializer for API Exceptions
    """

    status = serializers.IntegerField(required=True)

    url = serializers.CharField(required=True)

    message = serializers.CharField(required=True)