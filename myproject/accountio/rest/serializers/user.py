from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from accountio.models import User


class PublicUserRegistrationSerializer(serializers.Serializer):
    """This serializer will be used to serialize data for User registration"""

    first_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    phone = PhoneNumberField(allow_blank=True, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=5,
        max_length=100,
        write_only=True,
    )

    def create(self, validated_data):
        """Get or create a user by their email address, and return the validated data."""
        User.objects.get_or_create(
            email=validated_data["email"],
            defaults={
                "phone": validated_data.get("phone", ""),
                "password": make_password(validated_data.get("password")),
                "first_name": validated_data.get("first_name", ""),
                "last_name": validated_data.get("last_name", ""),
                "email": validated_data.get("email"),
            },
        )

        return validated_data


class UserAccountsSerializer(serializers.ModelSerializer):
    """Serializer for showing all user accounts."""

    class Meta:
        model = User
        fields = ("uid", "slug", "first_name", "last_name", "phone", "email", "status")
        read_only_fields = fields
