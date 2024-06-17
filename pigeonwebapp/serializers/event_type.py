from rest_framework import serializers
from pigeonwebapp.models import EventType

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'