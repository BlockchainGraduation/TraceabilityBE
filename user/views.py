from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer,
    ResponseUserSerializer,
    MyTokenObtainPairSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import User

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        tags=["auth"],
        operation_summary="User Register",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"message": serializer.errors})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(tags=["auth"], operation_summary="User Login")
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # access = response.data['access']
        response.set_cookie("access", response.data["access"], httponly=False)
        response.set_cookie("refresh", response.data["refresh"], httponly=False)
        return response


class MyTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=["auth"], operation_summary="User Refresh")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["auth"], operation_summary="User Logout")
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                response = Response()
                response.data = {"detail": "Successfully logged out."}
                response.status_code = status.HTTP_200_OK
                response.delete_cookie("access")
                response.delete_cookie("refresh")
                return response
            except Exception as e:
                return Response(
                    {"detail": "Invalid refresh token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # serializer = RegisterSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        user = User.objects.get(id=request.user.pk)
        serializer = ResponseUserSerializer(user)
        content = {
            "user": str(request.user.pk),  # `django.contrib.auth.User` instance.
            "auth": str(request.auth),  # None
        }
        return Response(serializer.data)
