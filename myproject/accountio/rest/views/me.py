from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from accountio.rest.serializers.me import MeDashboardSerializer


User = get_user_model()


class MeDashboardView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeDashboardSerializer

    def get_object(self):
        try:
            return User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            raise NotFound(detail="Something went Wrong!")
