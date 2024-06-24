from rest_framework import serializers
from pigeonwebapp.models import QueuedEmail
from pigeonwebapp.serializers.mailing_list import MailingListSerializer

class EmailSerializer(serializers.ModelSerializer):
    mail_to = MailingListSerializer(read_only=True)

    class Meta:
        model = QueuedEmail
        fields = '__all__'
        read_only_fields = ('__all__',)