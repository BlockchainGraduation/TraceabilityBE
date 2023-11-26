from rest_framework import serializers
from .models import Cart
from product.models import Product
from product.serializers import SimpleProductSerializers
from transaction.views import check_accept_create_product


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
        product = Product.objects.filter(
            pk=self.context["request"].data["product_id"]
        ).first()
        if product:
            if check_accept_create_product(
                self.context["request"], product.product_type
            ):
                cart = Cart.objects.filter(
                    create_by=self.context["request"].user, product_id=product
                )
                if cart:
                    raise serializers.ValidationError({"detail": "CART_EXISTS"})
                else:
                    validated_data["create_by"] = self.context["request"].user
                    cart = Cart.objects.create(**validated_data)
                    return cart
            else:
                raise serializers.ValidationError({"detail": "NOT_ALLOWED"})
        else:
            raise serializers.ValidationError({"detail": "PRODUCT_NOT_FOUND"})
