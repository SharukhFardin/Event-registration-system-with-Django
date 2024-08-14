from django.urls import path

from accountio.rest.views.user import (
    PublicUserRegistrationView,
    UserAccountList,
    UserAccountRetrieve,
)

urlpatterns = [
    path("", UserAccountList.as_view(), name="user_list"),
    path("<uuid:account_uid>", UserAccountRetrieve.as_view(), name="user_retrieve"),
    path(
        "user-registration",
        PublicUserRegistrationView.as_view(),
        name="user.onboarding",
    ),
]
