from rest_framework import serializers
from rest_framework.exceptions import APIException

from blockchain_web3.traceability import TraceabilityProvider
from cart.models import Cart
from product.models import Product
from product.serializers import SimpleProductSerializers
from user.models import User
from user.serializers import ResponseUserSerializer
from .models import Transaction


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
            self.context["request"].user.confirm_status != "DONE"
            or self.context["request"].user.is_active is False
            or self.context["request"].user.is_delete is True
        ):
            raise APIException("BLACK_USER")
        else:
            cart_id = validated_data.get("cart_id", None)
            if cart_id is not None:
                Cart.objects.filter(pk=cart_id).first().delete()
            user = User.objects.filter(pk=self.context["request"].user.pk).first()
            user.account_balance = user.account_balance - validated_data["price"]
            product = Product.objects.filter(pk=validated_data["product_id"].id).first()
            product.quantity = product.quantity - validated_data["quantity"]
            product.save()
            user.save()
            # data = validated_data
            validated_data["create_by"] = self.context["request"].user
            # print(data)
            # product = Product.objects.filter(pk=self.request.data["product_id"]).first()
            # if product:
            #     if product.quantity >= request.data["product_id"]:
            #         return super().create(request, *args, **kwargs)
            #     print(product.quantity)

            result = super().create(validated_data)
            tx_hash = TraceabilityProvider().buy_product(
                product_id=str(product.id),
                id_trans=str(result.id),
                buyer=str(self.context["request"].user.id),
                quantity=validated_data["quantity"],
            )
            result.tx_hash = tx_hash
            result.save()
            return result


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
