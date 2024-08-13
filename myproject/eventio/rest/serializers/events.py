from rest_framework import serializers

from eventio.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date",
            "time",
            "location",
            "available_slots",
        ]
