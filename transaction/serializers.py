from rest_framework import serializers
from .models import Transaction
from product.models import Product
from rest_framework.exceptions import APIException
from user.models import User
from cart.models import Cart
from product.serializers import SimpleProductSerializers, ProductSerializers
from user.serializers import ResponseUserSerializer
from product.serializers import TrackListingProductField


# from user.serializers import ResponseUserDetailSerializer


class ChangeStatusTransactionSerializer(serializers.Serializer):
    status = serializers.BooleanField(write_only=True)


class DetailTransactionSerializer(serializers.ModelSerializer):
    create_by = ResponseUserSerializer(read_only=True)
    product_id = SimpleProductSerializers(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        lookup_field = "product_id"
        extra_kwargs = {
            "create_by": {"read_only": True},
            "active": {"read_only": True},
            # "is_reject": {"read_only": True},
        }


class TransactionSerializer(serializers.ModelSerializer):
    create_by = ResponseUserSerializer(read_only=True)
    cart_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Transaction
        fields = "__all__"
        lookup_field = "product_id"
        extra_kwargs = {
            "create_by": {"read_only": True},
            "active": {"read_only": True},
            # "is_reject": {"read_only": True},
        }

    def create(self, validated_data):
        if (
            user.confirm_status != "DONE"
            or user.is_active is False
            or user.is_delete is True
        ):
            raise APIException("BLACK_USER")
        else:
            cart_id = validated_data.get("cart_id", None)
            if cart_id is not None:
                Cart.objects.filter(pk=cart_id).first().delete()
            user = User.objects.filter(pk=self.context["request"].user.pk).first()
            data = validated_data
            data["create_by"] = user
            # print(data)
            # product = Product.objects.filter(pk=self.request.data["product_id"]).first()
            # if product:
            #     if product.quantity >= request.data["product_id"]:
            #         return super().create(request, *args, **kwargs)
            #     print(product.quantity)
            return super().create(validated_data)


class ItemMultiTransactionSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Transaction
        fields = "__all__"
        extra_kwargs = {
            "active": {"read_only": True},
            "is_reject": {"read_only": True},
            "create_by": {"read_only": True},
        }


class MultiTransactionSerializer(serializers.Serializer):
    list_transactions = serializers.ListField(child=ItemMultiTransactionSerializer())

    class Meta:
        fields = "__all__"
