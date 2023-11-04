from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import ProductImage


# @parser_classes((MultiPartParser,))
class ProductImageSerializers(serializers.ModelSerializer):
    # datasheets = ListField(child=serializers.ImageField())

    class Meta:
        model = ProductImage
        fields = "__all__"
