from rest_framework import serializers, status
from comment.models import Comment
from notification.models import Notification, COMMENT_PRODUCT
from rest_framework.exceptions import APIException
from utils.pusher import PusherClient


class TrackListingUserField(serializers.RelatedField):
    def to_representation(self, value):
        from user.serializers import ResponseUserSerializer

        return ResponseUserSerializer(value).data


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "user_id": {"read_only": True},
        }

    def create(self, validated_data):
        try:
            user = self.context["request"].user
            if (
                user.confirm_status != "DONE"
                or user.is_active is False
                or user.is_delete is True
            ):
                raise APIException("BLACK_USER")
            else:
                validated_data["user_id"] = user
                Notification.objects.create(
                    create_by=self.context["request"].user,
                    product_id=validated_data["product_id"],
                    notification_type=COMMENT_PRODUCT,
                )
                comment = Comment.objects.create(**validated_data)
                pusher = PusherClient()
                pusher.push_notification(
                    "general-channel",
                    validated_data["product_id"].create_by.email,
                    {"message": "NEW_COMMENT"},
                )
                return comment

        except Exception as e:
            raise serializers.ValidationError("DATA_INVALID", status.HTTP_404_NOT_FOUND)


class DetailCommentSerializers(serializers.ModelSerializer):
    user_id = TrackListingUserField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "user_id": {"read_only": True},
        }
