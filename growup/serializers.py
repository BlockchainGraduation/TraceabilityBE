from rest_framework import serializers
from .models import GrowUp


class GrowUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = GrowUp
        fields = "__all__"
