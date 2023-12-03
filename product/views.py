from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from blockchain_web3.product_provider import ProductProvider
from transaction.models import Transaction, PENDDING, REJECT, ACCEPT, DONE
from .models import Product
from .serializers import (
    ProductSerializers,
    SimpleProductSerializers,
    DetailProductSerializers,
)


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
    queryset = Product.objects.filter(is_delete=False).order_by("-create_at")
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


class HistoryProductView(APIView):
    @swagger_auto_schema(tags=["product"], operation_summary="History product")
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(
            is_delete=False, pk=kwargs["product_id"]
        ).first()
        if product is None:
            return Response({"detail": []}, status=status.HTTP_200_OK)
        serializer = SimpleProductSerializers(product).data
        deep = True
        data = [serializer]
        while deep is True:
            if serializer["transaction_id"] is not None:
                transaction = Transaction.objects.filter(
                    pk=serializer["transaction_id"]
                ).first()
                product = Product.objects.filter(
                    is_delete=False, pk=transaction.product_id.id
                ).first()
                serializer = SimpleProductSerializers(product).data
                data.append(serializer)
            else:
                deep = False

        return Response({"detail": data}, status=status.HTTP_200_OK)


# Create your views here.
class ProductOwnerViews(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_delete=False)
    serializer_class = DetailProductSerializers
    permission_classes = [IsOwnerProduct, permissions.IsAuthenticated]


class ProductStatisticalViews(APIView):
    @swagger_auto_schema(
        tags=["product"],
        operation_summary="Statistical Product",
    )
    def get(self, request, *args, **kwargs):
        transaction_count = Transaction.objects.filter(product_id=kwargs["pk"]).count()
        pendding_transaction_count = Transaction.objects.filter(
            product_id=kwargs["pk"], status=PENDDING
        ).count()
        reject_transaction_count = Transaction.objects.filter(
            product_id=kwargs["pk"], status=REJECT
        ).count()
        done_transaction_count = Transaction.objects.filter(
            product_id=kwargs["pk"], status=DONE
        ).count()
        accept_transaction_count = Transaction.objects.filter(
            product_id=kwargs["pk"], status=ACCEPT
        ).count()

        return Response(
            {
                "transaction": {
                    "transaction_count": transaction_count,
                    "pendding_transaction_count": pendding_transaction_count,
                    "reject_transaction_count": reject_transaction_count,
                    "done_transaction_count": done_transaction_count,
                    "accept_transaction_count": accept_transaction_count,
                }
            }
        )


class ProductViews(viewsets.ModelViewSet):
    # queryset = Product.objects.filter()
    serializer_class = ProductSerializers
    simple_serializer_class = SimpleProductSerializers
    detail_serializer_class = DetailProductSerializers

    # permission_classes = [IsOwner]
    # def create(self, request, *args, **kwargs):
    #     image = Image.objects.create(request.FILES)
    #     return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == "list" or self.action == "retrieve":
            return Product.objects.filter(active=True, is_delete=False)
        return Product.objects.filter(is_delete=False)

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
        if self.action == "retrieve":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class

        return super(viewsets.ModelViewSet, self).get_serializer_class()

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, args, kwargs)
        product = Product.objects.get(id=kwargs["pk"])
        tx_hash = ProductProvider().update_product(
            product_id=product.id,
            hash_info="",
            quantity=product.quantity,
            price=product.price,
            status=1 if product.active else 0,
        )
        product.tx_hash = tx_hash
        product.save()
        return HttpResponse("SUCCESS")


class ProductTypeViews(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product_type", "create_by"]
    search_fields = ["name", "price"]
    queryset = Product.objects.filter(active=True, is_delete=False)
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

    def get_queryset(self):
        if self.request.query_params:
            return Product.objects.filter(active=True, is_delete=False)
        return Product.objects.none()


class ProductSearchViews(generics.ListAPIView):
    queryset = Product.objects.filter(active=True, is_delete=False)
    serializer_class = SimpleProductSerializers

    @swagger_auto_schema(
        tags=["product"],
        operation_summary="Search Product",
        manual_parameters=[
            openapi.Parameter(
                "name",
                in_=openapi.IN_QUERY,
                description="Lọc kiểu",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.query_params:
            # print(self.request.query_params)
            return Product.objects.filter(
                active=True,
                is_delete=False,
                name__icontains=self.request.query_params["name"],
            )
        return Product.objects.none()
