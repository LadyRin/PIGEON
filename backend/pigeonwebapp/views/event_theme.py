from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.event_theme import EventTheme
from pigeonwebapp.serializers.event_theme import EventThemeSerializer

class EventThemeViewSet(viewsets.ModelViewSet):
    serializer_class = EventThemeSerializer
    queryset = EventTheme.objects.all()