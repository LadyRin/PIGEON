from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.event_type import EventType
from pigeonwebapp.serializers.event_type import EventTypeSerializer

class EventTypeViewSet(viewsets.ModelViewSet):
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()

    def get_permissions(self):
        if self.action in ['get', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]