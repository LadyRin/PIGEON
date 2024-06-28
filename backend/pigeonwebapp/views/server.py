from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from pigeonwebapp.models import Server
from pigeonwebapp.serializers.server import ServerSerializer

class ServerViewSet(viewsets.ModelViewSet):
    serializer_class = ServerSerializer
    queryset = Server.objects.all()
    permission_classes = [IsAdminUser]

    