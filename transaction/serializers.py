from rest_framework import serializers
from .models import Transaction
from product.models import Product
from user.models import User
from product.serializers import SimpleProductSerializers, ProductSerializers
from user.serializers import ResponseUserSerializer
from product.serializers import TrackListingProductField


# from user.serializers import ResponseUserDetailSerializer


class ChangeStatusTransactionSerializer(serializers.Serializer):
    status = serializers.BooleanField(write_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    create_by = ResponseUserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        lookup_field = "product_id"
        extra_kwargs = {
            "create_by": {"read_only": True},
            # "active": {"read_only": True},
            # "is_reject": {"read_only": True},
        }

    def create(self, validated_data):
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
