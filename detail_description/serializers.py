from rest_framework import serializers
from .models import DetailDescription
from grow_up_image.serializers import GrowUpImageSerializers
from grow_up_image.models import GrowupImage
from product.models import Product


class DeitaiDescriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetailDescription
        fields = "__all__"
