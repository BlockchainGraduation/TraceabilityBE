from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer,
    RegisterRuleSerializer,
    ResponseUserSerializer,
    UpdateUserSerializer,
    MyTokenObtainPairSerializer,
    ConfirmOTPSerializer,
    LogoutSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import User, PENDING
from product.models import Product
from product.serializers import ProductSerializers
from .utils import generate_otp, send_otp_email


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class ConfirmOTP(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ConfirmOTPSerializer,
        tags=["auth"],
        operation_summary="User ConfirmOTP",
    )
    def post(self, request):
        serializer = ConfirmOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.data["password"] == serializer.data["re_password"]:
                user = User.objects.filter(
                    email=serializer.data["email"], otp=serializer.data["otp"]
                ).first()

                if user:
                    user.set_password(serializer.data["password"])
                    user.is_active = True
                    user.save()

                    return Response(
                        {
                            "user": ResponseUserSerializer(user).data,
                            "token": get_tokens_for_user(user),
                        },
                        status=status.HTTP_201_CREATED,
                    )
                # serializer.save()
                return Response(
                    {"detail": "WRONG_OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"detail": serializer.errors})


class RegisterRuleView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterRuleSerializer,
        tags=["user"],
        operation_summary="User Register Rule",
    )
    def post(self, request):
        serializer = RegisterRuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(id=request.user.pk)
            user.confirm_status = PENDING
            user.survey = serializer.data["survey"]
            user.save()
            return Response(
                {"detail": "REGISTER_RULE_SUCCESS"}, status=status.HTTP_201_CREATED
            )
        return Response({"detail": serializer.errors})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        tags=["auth"],
        operation_summary="User Register",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        user = User.objects.filter(email=request.data["email"]).first()
        if user:
            if user.is_active is False:
                otp = generate_otp()
                send_otp_email(request.data["email"], otp)
                user.username = request.data["username"]
                user.otp = otp
                user.save()
                return Response(
                    {"detail": "ACCOUNT_CREATED"}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"detail": "ACCOUNT_EXISTS"}, status=status.HTTP_400_BAD_REQUEST
            )

        else:
            if serializer.is_valid(raise_exception=True):
                otp = generate_otp()
                send_otp_email(serializer.data["email"], otp)
                User.objects.create(
                    **serializer.data, fullname=serializer.data["email"], otp=otp
                )
                # serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors})


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

    @swagger_auto_schema(
        tags=["auth"], request_body=LogoutSerializer, operation_summary="User Logout"
    )
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


class UpdateUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        return

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs["pk"]).first()
        if user:
            product = Product.objects.filter(create_by=kwargs["pk"])
            return Response(
                {
                    "user": ResponseUserSerializer(user).data,
                    "products": ProductSerializers(product, many=True).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "USER_NOT_FOUND"}, status=status.HTTP_400_BAD_REQUEST
        )

    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)
