from rest_framework import serializers
from .models import Notification
from user.serializers import ResponseUserSerializer
from product.serializers import SimpleProductSerializers


class NotificationSerializer(serializers.ModelSerializer):
    create_by = ResponseUserSerializer(read_only=True)
    product_id = SimpleProductSerializers(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        extra_kwargs = {
            "create_by": {"read_only": True},
        }


class DeleteNotificationSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField(required=True)
