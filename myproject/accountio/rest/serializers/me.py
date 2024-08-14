from rest_framework import serializers

from accountio.models import User

from eventio.models import EventRegistration
from eventio.rest.serializers.events import EventSlimSerializer


class MeDashboardSerializer(serializers.ModelSerializer):
    """Serializer for showing all user accounts."""

    registered_events = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "uid",
            "slug",
            "first_name",
            "last_name",
            "phone",
            "email",
            "status",
            "registered_events",
        )
        read_only_fields = fields

    def get_registered_events(self, obj):
        # Filter all EventRegistration instances for the current user
        registrations = EventRegistration.objects.filter(user=obj)

        # Extract the event instances from these registrations
        events = [registration.event for registration in registrations]

        # Serialize the events using EventSlimSerializer
        return EventSlimSerializer(events, many=True).data
