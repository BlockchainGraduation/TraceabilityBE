from rest_framework import serializers
from .models import Cart
from product.serializers import SimpleProductSerializers


class DetailCartSerializers(serializers.ModelSerializer):
    product_id = SimpleProductSerializers(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        extra_kwargs = {
            "create_by": {"read_only": True},
            # "active": {"rea   d_only": True},
        }

    def create(self, validated_data):
        validated_data["create_by"] = self.context["request"].user
        cart = Cart.objects.create(**validated_data)
        return cart
