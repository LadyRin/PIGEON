from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.event_theme import EventTheme
from pigeonwebapp.serializers.event_theme import EventThemeSerializer

class EventThemeViewSet(viewsets.ModelViewSet):
    serializer_class = EventThemeSerializer
    queryset = EventTheme.objects.all()

    def get_permissions(self):
        if self.action in ['get', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]