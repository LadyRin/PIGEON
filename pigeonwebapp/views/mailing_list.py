from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pigeonwebapp.models.mailing_list import MailingList
from pigeonwebapp.serializers.mailing_list import MailingListSerializer

class MailingListViewSet(viewsets.ModelViewSet):
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()