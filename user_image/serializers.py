from rest_framework import serializers
from .models import UserImage


# @parser_classes((MultiPartParser,))
class UserImageSerializers(serializers.ModelSerializer):
    # datasheets = ListField(child=serializers.ImageField())

    class Meta:
        model = UserImage
        fields = "__all__"
