from rest_framework import serializers
from pigeonwebapp.models import MailingList

class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = '__all__'