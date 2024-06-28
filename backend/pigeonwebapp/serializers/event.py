from rest_framework import serializers
from pigeonwebapp.serializers.event_type import EventTypeSerializer
from pigeonwebapp.serializers.event_theme import EventThemeSerializer
from pigeonwebapp.serializers.mailing_list import MailingListSerializer
from pigeonwebapp.serializers.user import UserSerializer
from pigeonwebapp.services.EmailRegisterService import register_emails_for_event

from pigeonwebapp.models import Event

class EventReadSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer(read_only=True)
    theme = EventThemeSerializer(read_only=True)
    mailing_list = MailingListSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('__all__',)

class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'event_type', 'theme', 'mailing_list', 'speaker_first_name', 'speaker_last_name', 'speaker_from', 'speaker_comment', 'date', 'start_time', 'end_time', 'description', 'attachment')

    def create(self, validated_data):
        validated_data['owner'] = self.context['user']
        event = super().create(validated_data)

        # Register emails for event
        register_emails_for_event(event)
        return event


class EventFlatSerializer(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    theme = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Event
        fields = ('title', 'event_type', 'theme', 'speaker_first_name', 'speaker_last_name', 'speaker_from', 'speaker_comment', 'date', 'start_time', 'end_time', 'description')
        read_only_fields = ('__all__',)