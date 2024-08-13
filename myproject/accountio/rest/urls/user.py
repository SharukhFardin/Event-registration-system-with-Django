from django.urls import path

from accountio.rest.views.user import (
    PublicUserRegistrationView,
)

urlpatterns = [
    path(
        "registration",
        PublicUserRegistrationView.as_view(),
        name="user.onboarding",
    ),
]
