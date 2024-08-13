from django.urls import path

from ..views.events import (
    EventList,
    EventDetails,
    EventRegisterView,
    EventUnregisterView,
)

urlpatterns = [
    path("", EventList.as_view(), name="event-list"),
    path("<uuid:uid>", EventDetails.as_view(), name="event-details"),
    path("<uuid:uid>/register", EventRegisterView.as_view(), name="event-register"),
    path(
        "<uuid:uid>/unregister", EventUnregisterView.as_view(), name="event-unregister"
    ),
]
