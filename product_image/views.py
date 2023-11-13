from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ProductImageSerializers
from .models import ProductImage


# Create your views here.
class ProductViews(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers
    # permission_classes = [IsOwner]
