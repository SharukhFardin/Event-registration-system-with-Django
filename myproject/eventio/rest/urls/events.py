from django.urls import path

from ..views.events import EventList

urlpatterns = [
    path("", EventList.as_view(), name="event-create"),
]
