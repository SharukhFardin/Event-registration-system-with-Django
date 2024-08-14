from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # User related APIs
    path("api/v1/me/", include("accountio.rest.urls.me")),
    path("api/v1/accounts/", include("accountio.rest.urls.user")),
    # Event related APIs
    path("api/v1/events/", include("eventio.rest.urls.events")),
    # Swagger
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path(
        "api/docs/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
