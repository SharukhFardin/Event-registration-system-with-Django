from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response

from accounts.models import User

from .mixins import PublicApiMixin, ApiErrorsMixin
from .utils import google_get_access_token, google_get_user_info

from .serializers import GoogleUserSerializer, InputSerializer


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data

    return access_token, refresh_token


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    serializer_class = InputSerializer

    def get(self, request, *args, **kwargs):
        input_serializer = self.serializer_class(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")

        login_url = f"{settings.BASE_FRONTEND_URL}/login"

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{login_url}?{params}")

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/google/"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data["email"])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                "user": GoogleUserSerializer(user).data,
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            }
            return Response(response_data)
        except User.DoesNotExist:
            username = user_data["email"].split("@")[0]
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")

            name = f"{first_name} {last_name}"

            user = User.objects.create(
                username=username,
                email=user_data["email"],
                name=name,
                # registration_method="google",
                phone=None,
            )

            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                "user": GoogleUserSerializer(user).data,
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            }
            return Response(response_data)
