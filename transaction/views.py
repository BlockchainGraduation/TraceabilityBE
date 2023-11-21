from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from .models import Transaction
from .serializers import TransactionSerializer, ChangeStatusTransactionSerializer
from product.models import Product
from product.serializers import SimpleProductSerializers
from user.models import User, RETAILER, FACTORY, DISTRIBUTER


def check_accept_create_product(request, product_type):
    if request.user.role == DISTRIBUTER and product_type == FACTORY:
        return True
    if request.user.role == RETAILER and product_type == FACTORY:
        return True
    return False


# Create your views here.

from rest_framework import generics


class FilterTransactionViews(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product_id"]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # serializer_class = TransactionSerializer

    @swagger_auto_schema(
        tags=["transaction"],
        operation_summary="Filter Product",
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                in_=openapi.IN_QUERY,
                description="Lọc theo product_id",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransactionMeView(generics.ListAPIView):
    # lookup_field = "product_id"
    filter_backends = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(
            # desc__contains=filter,
            product_id__create_by=request.user.pk,
            active=False,
            is_reject=False,
        )
        return Response(
            TransactionSerializer(transactions, many=True).data,
            status=status.HTTP_202_ACCEPTED,
        )


class TransactionView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # lookup_field = "id"

    def create(self, request, *args, **kwargs):
        request.data["product_id"]
        # super().create(request, *args, **kwargs)
        product = Product.objects.filter(pk=request.data["product_id"]).first()
        if request.user.account_balance < request.data["price"]:
            return Response(
                {"detail": "BALANCE_NOT_ENOUGHT"}, status=status.HTTP_400_BAD_REQUEST
            )
        if product:
            if check_accept_create_product(
                request=request, product_type=product.product_type
            ):
                if product.quantity >= request.data["quantity"]:
                    return super().create(request, *args, **kwargs)
            else:
                return Response(
                    {"detail": "NOT_ALLOWED"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"detail": "DATA_INVALID"}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class RetrieveTransactionView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # lookup_field = "id"
    @swagger_auto_schema(tags=["transaction"], operation_summary="Get Transaction")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChangeStatusTransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["transaction"],
        request_body=ChangeStatusTransactionSerializer,
        operation_summary="Accept Transaction",
    )
    def patch(self, request, pk, *args, **kwargs):
        is_accept = request.data["status"]
        user = User.objects.filter(pk=request.user.pk).first()
        transaction = Transaction.objects.filter(pk=pk).first()
        product = Product.objects.filter(
            pk=transaction.product_id_id, create_by=user.pk
        ).first()
        if product:
            if is_accept is True:
                if product.quantity > transaction.quantity:
                    product.quantity = product.quantity - transaction.quantity
                    transaction.active = True
                    product.save()
                    transaction.save()
                    return Response({"detail": "DONE"}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        {"detail": "QUANTITY_INVALID"},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                transaction.is_reject = True
                transaction.save()
                return Response({"detail": "OK"}, status=status.HTTP_202_ACCEPTED)
        return Response({"detail": "Loi"}, status=status.HTTP_400_BAD_REQUEST)
