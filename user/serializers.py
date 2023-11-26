from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from product.serializers import ProductSerializers, SimpleProductSerializers
from user_image.serializers import UserImageSerializers
from user_image.models import UserImage
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


class ConfirmUserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(format="hex_verbose", required=True)
    status = serializers.BooleanField(required=True)


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


class ForgetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30, min_length=None, allow_blank=False)


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=20, min_length=None, allow_blank=False
    )
    new_password = serializers.CharField(max_length=20, min_length=4, allow_blank=False)
    re_new_password = serializers.CharField(
        max_length=20, min_length=4, allow_blank=False
    )


class ResponseUserDetailSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializers(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ["user_permissions", "groups", "password", "otp"]


class ResponseUserSerializer(serializers.ModelSerializer):
    user_banner = UserImageSerializers(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ["user_permissions", "groups", "password", "otp"]
        # fields = '__all__'
        extra_kwargs = {
            "password": {"read_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    user_banner = UserImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=None, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        max_length=8,
    )

    class Meta:
        model = User
        # fields =
        exclude = ["password"]
        read_only_fields = (
            "user_permissions",
            "groups",
            "password",
            "username",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "role",
            "otp",
            "confirm_status",
            "email",
            "username",
            "last_login",
        )

    def update(self, instance, validated_data):
        if self.initial_data.get("uploaded_images") is None:
            return super().update(instance, validated_data)
        uploaded_images = validated_data.pop("uploaded_images")
        user = User.objects.filter(pk=instance.pk).first()
        UserImage.objects.filter(user=user).delete()
        for image in uploaded_images:
            UserImage.objects.create(user=user, image=image)
        return super().update(instance, validated_data)
