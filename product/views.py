from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ProductSerializers, SimpleProductSerializers
from .models import Product
from user.models import User


class IsOwnerProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs["pk"]
        # print(view.kwargs["pk"])
        # print(view.kwargs["pk"])
        # print("user", request.user.id)
        superuser = request.user.is_superuser
        product = Product.objects.filter(pk=pk, create_by=request.user.id).first()
        return True if product or superuser else False

    # def has_object_permission(self, request, view, obj):
    #     print(view.kwargs)
    #     return True


class ProductMeViews(generics.ListAPIView):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = SimpleProductSerializers
    filterset_fields = ["create_by"]

    @swagger_auto_schema(
        tags=["product"],
        operation_summary="Product me",
        manual_parameters=[
            openapi.Parameter(
                "create_by",
                in_=openapi.IN_QUERY,
                description="Lọc product theo user",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Create your views here.
class ProductViews(viewsets.ModelViewSet):
    # queryset = Product.objects.filter()
    serializer_class = ProductSerializers
    simple_serializer_class = SimpleProductSerializers

    # permission_classes = [IsOwner]
    # def create(self, request, *args, **kwargs):
    #     image = Image.objects.create(request.FILES)
    #     return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == "list" or self.action == "retrieve":
            return Product.objects.filter(active=True)
        return Product.objects.all()

    def get_permissions(self):
        if (
            self.action == "partial_update"
            or self.action == "destroy"
            or self.action == "update"
        ):
            return [IsOwnerProduct(), permissions.IsAuthenticated()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == "list":
            if hasattr(self, "simple_serializer_class"):
                return self.simple_serializer_class

        return super(viewsets.ModelViewSet, self).get_serializer_class()


class ProductTypeViews(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product_type", "create_by"]
    search_fields = ["name", "price"]
    queryset = Product.objects.filter(active=True)
    serializer_class = SimpleProductSerializers

    @swagger_auto_schema(
        tags=["product"],
        operation_summary="Filter Product",
        manual_parameters=[
            openapi.Parameter(
                "product_type",
                in_=openapi.IN_QUERY,
                description="Lọc kiểu",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "name",
                in_=openapi.IN_QUERY,
                description="Lọc name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "price",
                in_=openapi.IN_QUERY,
                description="Lọc giá",
                type=openapi.TYPE_INTEGER,
            ),
            # Các tham số khác nếu cần
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
