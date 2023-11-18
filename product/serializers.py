from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import Product
from user.models import User, SEEDLING_COMPANY
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from product_image.serializers import ProductImageSerializers
from product_image.models import ProductImage
from growup.serializers import GrowUpSerializers
from comment.serializers import CommentSerializers
from rest_framework.fields import ListField

# from user.serializers import ResponseUserSerializer

# from transaction.serializers import TransactionSerializer


# @parser_classes((MultiPartParser,))
class TrackListingField(serializers.RelatedField):
    def to_representation(self, value):
        from user.serializers import ResponseUserSerializer

        return ResponseUserSerializer(value).data


class SimpleProductSerializers(serializers.ModelSerializer):
    banner = ProductImageSerializers(many=True, read_only=True)
    create_by = TrackListingField(read_only=True)
    # uploaded_images = serializers.ListField(
    #     child=serializers.ImageField(
    #         max_length=1000000, allow_empty_file=False, use_url=False
    #     ),
    #     write_only=True,
    # )

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "create_by": {"read_only": True},
        }
        depth = 10


class ProductSerializers(serializers.ModelSerializer):
    # from user.serializers import ResponseUserSerializer

    banner = ProductImageSerializers(many=True, read_only=True)
    growup = GrowUpSerializers(many=True, read_only=True)
    comments = CommentSerializers(many=True, read_only=True)
    create_by = TrackListingField(read_only=True)
    # transaction_id = TransactionSerializer(read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "create_by": {"read_only": True},
        }

    def create(self, validated_data):
        if self.context["request"].user.role != SEEDLING_COMPANY:
            checktransaction_id = validated_data.get("transaction_id", None)
            if checktransaction_id is None:
                raise APIException(
                    detail="transaction_id is required",
                )
        uploaded_images = validated_data.pop("uploaded_images")
        validated_data["create_by"] = User.objects.get(
            pk=self.context["request"].user.pk
        )
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        if self.initial_data.get("uploaded_images") is None:
            return super().update(instance, validated_data)
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.filter(
            pk=self.context["view"].kwargs.get("pk")
        ).first()
        ProductImage.objects.filter(product=product).delete()
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return super().update(instance, validated_data)
