from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import User
from .utils import generate_otp, send_otp_email


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["user"] = user.username
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "phone"]
        extra_kwargs = {
            "username": {"required": True},
            "phone": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        otp = generate_otp()
        user.otp = otp
        send_otp_email(validated_data["email"], otp)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["user_permissions", "groups", "password"]
        # fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
        read_only_fields = (
            "user_permissions",
            "groups",
            "password",
            "username",
            "date_joined",
        )
