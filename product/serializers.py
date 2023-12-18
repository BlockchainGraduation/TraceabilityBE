from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from blockchain_web3.product_provider import ProductProvider
from .models import Product
from user.models import User, FACTORY, RETAILER, DISTRIBUTER
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from product_image.serializers import ProductImageSerializers
from product_image.models import ProductImage
from growup.serializers import GrowUpSerializers
from detail_description.serializers import DeitaiDescriptionSerializers
from comment.serializers import CommentSerializers
from transaction.models import Transaction
from rest_framework.fields import ListField


# from user.serializers import ResponseUserSerializer

# from transaction.serializers import TransactionSerializer


# @parser_classes((MultiPartParser,))
class TrackListingProductField(serializers.RelatedField):
    def to_representation(self, value):
        from user.serializers import SimpleProductSerializers

        return SimpleProductSerializers(value).data


class TrackListingUserField(serializers.RelatedField):
    def to_representation(self, value):
        from user.serializers import ResponseUserSerializer

        return ResponseUserSerializer(value).data


class TrackListingTransactionField(serializers.RelatedField):
    def to_representation(self, value):
        from transaction.serializers import TransactionSerializer

        return TransactionSerializer(value).data


class SimpleProductSerializers(serializers.ModelSerializer):
    banner = ProductImageSerializers(many=True, read_only=True)
    create_by = TrackListingUserField(read_only=True)
    total_transaction = serializers.SerializerMethodField(read_only=True)

    def get_total_transaction(self, product):
        return product.transaction_product.count()

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
            # "active": {"read_only": True},
        }
        # depth = 10


class DetailProductSerializers(serializers.ModelSerializer):
    banner = ProductImageSerializers(many=True, read_only=True)
    growup = GrowUpSerializers(many=True, read_only=True)
    comments = CommentSerializers(many=True, read_only=True)
    detail_decriptions = DeitaiDescriptionSerializers(many=True, read_only=True)
    create_by = TrackListingUserField(read_only=True)
    transaction_id = TrackListingTransactionField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "create_by": {"read_only": True},
            "active": {"read_only": True},
        }
        depth = 10


class ProductSerializers(serializers.ModelSerializer):
    # from user.serializers import ResponseUserSerializer

    banner = ProductImageSerializers(many=True, read_only=True)
    growup = GrowUpSerializers(many=True, read_only=True)
    comments = CommentSerializers(many=True, read_only=True)
    detail_decriptions = DeitaiDescriptionSerializers(many=True, read_only=True)
    create_by = TrackListingUserField(read_only=True)
    # transaction_id = serializers.StringRelatedField(many=True)

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
            # "active": {"rea   d_only": True},
        }

    def create(self, validated_data):
        if (
            self.context["request"].user.confirm_status != "DONE"
            or self.context["request"].user.is_active is False
            or self.context["request"].user.is_delete is True
        ):
            raise APIException(
                detail="BLACK_USER",
            )
        else:
            check_transaction_id = validated_data.get("transaction_id", "")
            if self.context["request"].user.role != FACTORY:
                if check_transaction_id is None or check_transaction_id == "":
                    raise APIException(
                        detail="transaction_id is required",
                    )
                else:
                    transaction = Transaction.objects.filter(
                        pk=check_transaction_id.id
                    ).first()
                    transaction.active = True
                    transaction.save()

            uploaded_images = validated_data.pop("uploaded_images")
            validated_data["create_by"] = User.objects.get(
                pk=self.context["request"].user.pk
            )
            product = Product.objects.create(**validated_data)
            map_type = {FACTORY: 1, DISTRIBUTER: 2, RETAILER: 3}
            if check_transaction_id:
                check_transaction_id = str(check_transaction_id.id)
            else:
                check_transaction_id = ""

            tx_hash = ProductProvider().create_product(
                product_id=str(product.id),
                product_type=map_type[self.context["request"].user.role],
                quantity=product.quantity,
                price=product.price,
                hash_info="",
                trans_id=check_transaction_id,
                owner=str(self.context["request"].user.id),
                status=0,
            )
            product.tx_hash = tx_hash
            product.save()
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
