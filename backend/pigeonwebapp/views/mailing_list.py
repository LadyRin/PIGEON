from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.mailing_list import MailingList
from pigeonwebapp.serializers.mailing_list import MailingListSerializer

class MailingListViewSet(viewsets.ModelViewSet):
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()

    def get_permissions(self):
        if self.action in ['get', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]