from rest_framework import serializers, status
from comment.models import Comment


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
            validated_data["user_id"] = user
            comment = Comment.objects.create(**validated_data)
            return comment
        except Exception as e:
            raise serializers.ValidationError("DATA_INVALID", status.HTTP_404_NOT_FOUND)
