from rest_framework import generics
from rest_framework.permissions import AllowAny

from accountio.rest.serializers.user import (
    PublicUserRegistrationSerializer,
)


class PublicUserRegistrationView(generics.CreateAPIView):
    serializer_class = PublicUserRegistrationSerializer
    permission_classes = [AllowAny]
