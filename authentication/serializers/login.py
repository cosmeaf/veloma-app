from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        return value.lower().strip()

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password required.")

        user = User.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        user = authenticate(username=user.username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        attrs["user"] = user

        return attrs