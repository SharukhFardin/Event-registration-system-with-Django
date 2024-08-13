from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from eventio.models import Event

from ..serializers.events import EventSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.filter()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["date", "location", "available_slots"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["date", "available_slots"]
