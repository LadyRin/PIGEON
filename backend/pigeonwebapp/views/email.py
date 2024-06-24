from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.queued_email import QueuedEmail
from pigeonwebapp.serializers.email import EmailSerializer

class EmailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailSerializer
    queryset = QueuedEmail.objects.all()
    permission_classes = [IsAdminUser]