from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import Product
from user.models import User


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "create_by": {"read_only": True},
        }

    def create(self, validated_data):
        if self.context["request"].user.role != "SeedCompany":
            checktransaction_id = validated_data.get("transaction_id", None)
            if checktransaction_id is None:
                raise APIException(
                    detail="transaction_id is required",
                )
        validated_data["create_by"] = User.objects.get(
            pk=self.context["request"].user.pk
        )
        product = Product.objects.create(**validated_data)
        return product
