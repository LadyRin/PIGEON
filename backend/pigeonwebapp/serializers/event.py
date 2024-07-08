from datetime import datetime
from django.conf import settings
import pytz
from rest_framework import serializers
from pigeonwebapp.serializers.event_type import EventTypeSerializer
from pigeonwebapp.serializers.event_theme import EventThemeSerializer
from pigeonwebapp.serializers.mailing_list import MailingListSerializer
from pigeonwebapp.serializers.user import UserSerializer
from pigeonwebapp.services.emails import register_emails_for_event
from pigeonwebapp.services.booking import Booker
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
        fields = ('title', 'event_type', 'theme', 'mailing_list', 'speaker_first_name', 'speaker_last_name', 'speaker_from', 'speaker_comment', 'date', 'start_time', 'end_time', 'description', 'resource_id')
        extra_kwargs = {
            'resource_id': {'write_only': True, 'required': True},
        }

    def dt(self, date, time):
            tz = pytz.timezone(settings.TIME_ZONE)
            date_time = datetime.combine(date, time)
            return tz.localize(date_time)

    def validate(self, data):
        start_datetime = self.dt(data['date'], data['start_time'])
        end_datetime = self.dt(data['date'], data['end_time'])
        if start_datetime >= end_datetime:
            raise serializers.ValidationError("End time must be after start time")
        
        return data

    def create(self, validated_data):
        validated_data['owner'] = self.context['user']
        start_datetime = self.dt(validated_data['date'], validated_data['start_time'])
        end_datetime = self.dt(validated_data['date'], validated_data['end_time'])
        event = super().create(validated_data)

        if 'resource_id' in validated_data:
            booker = Booker()
            booker.authenticate()
            if not booker.is_available(validated_data['resource_id'], start_datetime, end_datetime):
                raise serializers.ValidationError("Resource is not available for this time")
            reservation_id = booker.book_resource(validated_data['resource_id'], event.title, start_datetime, end_datetime)
            event.reservation_id = reservation_id

        register_emails_for_event(event)
        return event
    
    def update(self, instance, validated_data):
        booker = Booker()
        booker.authenticate()

        if instance.reservation_id:
            booker.unbook(instance.reservation_id)

        if 'resource_id' in validated_data:
            start_datetime = self.dt(validated_data['date'], validated_data['start_time'])
            end_datetime = self.dt(validated_data['date'], validated_data['end_time'])
            if not booker.is_available(validated_data['resource_id'], start_datetime, end_datetime):
                raise serializers.ValidationError("Resource is not available for this time")
            reservation_id = booker.book_resource(validated_data['resource_id'], instance.title, start_datetime, end_datetime)
            validated_data['reservation_id'] = reservation_id

        event = super().update(instance, validated_data)
        register_emails_for_event(event)
        return event


class EventFlatSerializer(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    theme = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Event
        fields = ('title', 'event_type', 'theme', 'speaker_first_name', 'speaker_last_name', 'speaker_from', 'speaker_comment', 'date', 'start_time', 'end_time', 'description')
        read_only_fields = ('__all__',)