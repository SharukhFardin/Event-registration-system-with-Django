from django.urls import path

from accountio.rest.views.me import (
    MeDashboardView,
)

urlpatterns = [
    path("dashboard", MeDashboardView.as_view(), name="me-dashboard"),
]
