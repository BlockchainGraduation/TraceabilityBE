from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from product.serializers import ProductSerializers
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


class ConfirmOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(
        max_length=6, min_length=6, allow_blank=False, trim_whitespace=False
    )
    email = serializers.EmailField(max_length=30, min_length=None, allow_blank=False)
    password = serializers.CharField(
        max_length=20, min_length=5, allow_blank=False, trim_whitespace=False
    )
    re_password = serializers.CharField(
        max_length=20, min_length=5, allow_blank=False, trim_whitespace=False
    )


class RegisterRuleSerializer(serializers.Serializer):
    survey = serializers.JSONField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=20, min_length=5, allow_blank=False, trim_whitespace=False
    )
    email = serializers.EmailField(max_length=30, min_length=None, allow_blank=False)

    class Meta:
        # model = User
        fields = ["username", "email"]
        # extra_kwargs = {
        #     "username": {"required": True},
        # "phone": {"required": True},
        # "email": {"required": True},
        # "password": {"write_only": True, "required": True},
        # }

        # def create(self, validated_data):
        #     user = User.objects.filter(
        #         email=validated_data["email"], is_active=False
        #     ).first()
        #     if user:
        #         return user
        #     user = User.objects.create(**validated_data)
        #     otp = generate_otp()
        #     user.otp = otp
        #     send_otp_email(validated_data["email"], otp)
        #     # user.set_password(validated_data["password"])
        #     user.save()
        # return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


# class ResponseUserProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializers(many=True, read_only=True)

#     class Meta:
#         model = User
#         exclude = ["user_permissions", "groups", "password", "otp"]


class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["user_permissions", "groups", "password", "otp"]
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
