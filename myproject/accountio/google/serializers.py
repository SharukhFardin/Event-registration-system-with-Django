from rest_framework import serializers

from accounts.models import User


class GoogleUserSerializer(serializers.ModelSerializer):
    """This serializer is specifically used for google auth"""

    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
            "email",
        ]


class InputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
