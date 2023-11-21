from rest_framework import serializers
from .models import GrowUp
from grow_up_image.serializers import GrowUpImageSerializers
from grow_up_image.models import GrowupImage
from product.models import Product


class GrowUpSerializers(serializers.ModelSerializer):
    growup_images = GrowUpImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=10000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = GrowUp
        fields = "__all__"

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print(validated_data["product_id"])
        # product = Product.objects.filter(pk=validated_data["product_id"]).first()
        growup = GrowUp.objects.create(**validated_data)
        for image in uploaded_images:
            GrowupImage.objects.create(growup_id=growup, image=image)
        return growup
