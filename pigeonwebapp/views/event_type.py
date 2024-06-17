from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.event_type import EventType
from pigeonwebapp.serializers.event_type import EventTypeSerializer

class EventTypeViewSet(viewsets.ModelViewSet):
    serializer_class = EventType
    queryset = EventType.objects.all()