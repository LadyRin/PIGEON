from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.email import Email
from pigeonwebapp.serializers.email import EmailSerializer

class EmailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailSerializer
    queryset = Email.objects.all()
    permission_classes = [IsAdminUser]