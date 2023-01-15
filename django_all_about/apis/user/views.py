# python lib
from typing import Any

# django, drf lib
from django.shortcuts import render
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# app lib
from apis.user.serializers import (
    CustomRegisterSerializer,
    CustomLoginSerializer,
    CustomTokenRefreshSerializer,
)


class RegisterAPIView(RegisterView):
    # parser_classes = MultiPartParser
    serializer_class = CustomRegisterSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - 회원가입 시 token 제공을 위해 해당 함수 재정의
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token = TokenObtainPairSerializer.get_token(user)

        return Response(
            dict(access_token=str(token.access_token), refresh_token=str(token)),
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        # print(serializer)
        return super().perform_create(serializer)


class LoginAPIView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        """
        - 로그인 성공 시 token 제공을 위해 해당 함수 재정의
        """
        token = TokenObtainPairSerializer.get_token(self.user)
        return Response(
            dict(
                access_token=str(token.access_token),
                refresh_token=str(token),
            ),
            status=status.HTTP_200_OK,
        )


class CustomTokenRefreshView(TokenViewBase):
    serializer_class = CustomTokenRefreshSerializer
