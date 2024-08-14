from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from eventio.models import Event, EventRegistration

from ..serializers.events import EventSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.prefetch_related("eventregistration_set").filter()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["date", "location", "available_slots"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["date", "available_slots"]

    def get_serializer_context(self):
        # Pass the request context to the serializer
        return {"request": self.request}


class EventDetails(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "uid"


class EventRegisterView(APIView):
    """This view Register a event under an User."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_uid = self.kwargs.get("uid")

        # Fetch the event object
        try:
            event = Event.objects.get(uid=event_uid)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is already registered
        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if there are available slots
        if event.available_slots <= 0:
            return Response(
                {"detail": "No slots available."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Register the user
        EventRegistration.objects.create(user=request.user, event=event)

        # Update the event's available slots
        event.available_slots -= 1
        event.save()

        return Response(
            {"detail": "Successfully registered for the event."},
            status=status.HTTP_201_CREATED,
        )


class EventUnregisterView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event = Event.objects.get(uid=self.kwargs["uid"])
        registration = EventRegistration.objects.filter(
            event=event, user=self.request.user
        ).first()

        if registration:
            registration.delete()
            event.available_slots += 1
            event.save()
            return Response(
                {"detail": "Successfully unregistered from the event."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "You are not registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )
