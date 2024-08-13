from rest_framework import serializers

from eventio.models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "uid",
            "title",
            "description",
            "date",
            "time",
            "location",
            "available_slots",
            "is_registered",
        ]
        read_only_fields = ["uid"]

    def get_is_registered(self, obj):
        # Get the current user from the request context
        user = self.context["request"].user

        # Check if the user is registered for the event
        return EventRegistration.objects.filter(event=obj, user=user).exists()
