from rest_framework import serializers
from .models import GrowupImage


# @parser_classes((MultiPartParser,))
class GrowUpImageSerializers(serializers.ModelSerializer):
    # datasheets = ListField(child=serializers.ImageField())

    class Meta:
        model = GrowupImage
        fields = "__all__"
