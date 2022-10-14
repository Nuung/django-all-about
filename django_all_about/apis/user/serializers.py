
# django, drf lib
from django.conf import settings
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomRegisterSerializer(RegisterSerializer):
    username = password1 = password2 = None
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('id', 'email', 'name',)

    def get_cleaned_data(self):
        return dict(
            email=self.validated_data.get('email', ''),
            password=self.validated_data.get('password', ''),
            name=self.validated_data.get('name', ''),
        )

    def validate(self, data):
        """
        - password1, password2에 대한 validate 제거
        """
        return data


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)
    access = serializers.CharField(required=False)
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token", "refresh")
        data = super().validate(attrs)
        data["refresh_token"] = data.pop("refresh", None)
        data["access_token"] = data.pop("access", None)
        return data