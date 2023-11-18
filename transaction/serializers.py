from rest_framework import serializers
from .models import Transaction
from product.models import Product
from user.models import User
from product.serializers import ProductSerializers

# from user.serializers import ResponseUserDetailSerializer


class TransactionSerializer(serializers.ModelSerializer):
    product_id = ProductSerializers(read_only=True)
    # create_by = ResponseUserDetailSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        lookup_field = "product_id"
        extra_kwargs = {
            "create_by": {"read_only": True},
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
