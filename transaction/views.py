from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from cart.models import Cart
import collections.abc
from .models import Transaction, PENDDING, REJECT, ACCEPT, DONE
from .serializers import (
    TransactionSerializer,
    ChangeStatusTransactionSerializer,
    DetailTransactionSerializer,
    MultiTransactionSerializer,
)
from product.models import Product
from product.serializers import SimpleProductSerializers
from user.models import User, RETAILER, FACTORY, DISTRIBUTER


def check_accept_create_product(request, product_type):
    if request.user.role == DISTRIBUTER and product_type == FACTORY:
        return True
    if request.user.role == RETAILER and product_type == DISTRIBUTER:
        return True
    return False


# Create your views here.

from rest_framework import generics


class CreateMultiTransactionViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["transaction"],
        operation_summary="CreateMultiTransactionViews",
        request_body=MultiTransactionSerializer,
    )
    def post(self, request, *args, **kwargs):
        # data = request.data["list_transactions"]
        # result_list = []

        if type(request.data["list_transactions"]).__name__ in ("list", "tuple"):
            total_price = sum(
                item["price"] for item in request.data["list_transactions"]
            )
            if total_price < request.user.account_balance:
                for item_data in request.data["list_transactions"]:
                    product = Product.objects.filter(pk=item_data["product_id"]).first()
                    Transaction.objects.create(
                        quantity=item_data["quantity"],
                        price=item_data["price"],
                        product_id=product,
                        create_by=request.user,
                    )
                    Cart.objects.filter(
                        pk=item_data["cart_id"], create_by=request.user
                    ).delete()
                return Response(
                    {
                        "detail": "CREATED",
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "detail": "BALANCE_NOT_ENOUGHT",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            # Handle invalid data
            # Access serializer.errors for details on validation errors
            return Response(
                {
                    "detail": "DATA_INVALID",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class FilterTransactionViews(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "product_id"]
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
            ),
            openapi.Parameter(
                "status",
                in_=openapi.IN_QUERY,
                description="Lọc theo status",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransactionMeView(generics.ListAPIView):
    # lookup_field = "product_id"
    queryset = Transaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "create_by"]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetailTransactionSerializer

    @swagger_auto_schema(
        tags=["transaction"],
        operation_summary="Filter Product",
        manual_parameters=[
            openapi.Parameter(
                "status",
                in_=openapi.IN_QUERY,
                description="Lọc theo status",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "create_by",
                in_=openapi.IN_QUERY,
                description="Lọc theo create_by",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        # transaction_status = request.GET.get("status", None)

        # if transaction_status is None:
        #     transactions = Transaction.objects.filter(
        #         create_by=request.user.pk
        #         # product_id__create_by=request.user.pk,
        #     )
        # else:
        #     transactions = Transaction.objects.filter(
        #         create_by=request.user.pk,
        #         status=transaction_status
        #         # product_id__create_by=request.user.pk,
        #     )

        # return Response(
        #     DetailTransactionSerializer(transactions, many=True).data,
        #     status=status.HTTP_202_ACCEPTED,
        # )
        return super().get(self, request, *args, **kwargs)


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


class AllTransactionSellMe(generics.ListAPIView):
    serializer_class = DetailTransactionSerializer

    @swagger_auto_schema(
        tags=["transaction"], operation_summary="Get All Sell Transaction"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Transaction.objects.filter(product_id__create_by=self.request.user)


class RetrieveTransactionView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = DetailTransactionSerializer

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
                    transaction.status = ACCEPT
                    product.save()
                    transaction.save()
                    return Response({"detail": "DONE"}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        {"detail": "QUANTITY_INVALID"},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                user = User.objects.filter(pk=transaction.create_by.id).first()
                user.account_balance = user.account_balance - transaction.price
                product.quantity = product.quantity + transaction.quantity
                transaction.status = REJECT
                user.save()
                product.save()
                transaction.save()
                return Response({"detail": "OK"}, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"detail": "PRODUCT_NOT_EXISTS"}, status=status.HTTP_400_BAD_REQUEST
        )


class DoneTransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["transaction"], operation_summary="Done transaction")
    def patch(self, request, *args, **kwargs):
        transaction = Transaction.objects.filter(
            pk=kwargs["pk"], create_by=request.user
        ).first()
        if transaction:
            product = Product.objects.filter(pk=transaction.product_id.id).first()
            user = User.objects.filter(pk=product.create_by.id).first()
            user.account_balance = user.account_balance + transaction.price
            user.save()
            transaction.status = DONE
            transaction.save()
            return Response({"detail": "SUCCESS"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "TRANSACTION_NOT_EXISTS"}, status=status.HTTP_400_BAD_REQUEST
            )
