from rest_framework import serializers
from pigeonwebapp.models import EventTheme

class EventThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTheme
        fields = '__all__'