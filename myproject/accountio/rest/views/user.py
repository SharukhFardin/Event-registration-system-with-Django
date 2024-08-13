from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound

from accountio.rest.serializers.user import (
    PublicUserRegistrationSerializer,
    UserAccountsSerializer,
)

from sharedio.permissions.staff import IsStaff

User = get_user_model()


class PublicUserRegistrationView(generics.CreateAPIView):
    serializer_class = PublicUserRegistrationSerializer
    permission_classes = [AllowAny]


class UserAccountList(generics.ListAPIView):
    serializer_class = UserAccountsSerializer
    permission_classes = [IsStaff]
    queryset = User.objects.filter()


class UserAccountRetrieve(generics.RetrieveDestroyAPIView):
    serializer_class = UserAccountsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Override to get the object based on account_uid."""
        try:
            user = User.objects.get(uid=self.kwargs.get("account_uid"))
        except User.DoesNotExist:
            raise NotFound(detail="Account not found")
        return user

    def destroy(self, request, *args, **kwargs):
        """Overriding the delete method to perform a SOFT delete."""

        user = self.get_object()
        user.removed()  # Call the removed method to perform a soft delete

        return Response(status=status.HTTP_204_NO_CONTENT)
