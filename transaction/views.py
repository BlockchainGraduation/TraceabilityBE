from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from .models import Transaction
from .serializers import TransactionSerializer
from product.models import Product
from user.models import User, FISHERMEN, FACTORY, SEEDLING


def check_accept_create_product(request, product_type):
    if request.user.role == FISHERMEN and product_type == SEEDLING:
        return True
    if request.user.role == FACTORY and product_type == FISHERMEN:
        return True
    return False


# Create your views here.

from rest_framework import generics


class TransactionView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # lookup_field = "id"

    def create(self, request, *args, **kwargs):
        request.data["product_id"]
        # super().create(request, *args, **kwargs)
        product = Product.objects.filter(pk=request.data["product_id"]).first()
        if product:
            if check_accept_create_product(
                request=request, product_type=product.product_type
            ):
                if product.quantity >= request.data["quantity"]:
                    return super().create(request, *args, **kwargs)
            else:
                return Response(
                    {"message": "NOT_ALLOWED"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"message": "DATA_INVALID"}, status=status.HTTP_400_BAD_REQUEST)

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


class AcceptTransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["transaction"],
        operation_summary="Accept Transaction",
    )
    def patch(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=request.user.pk).first()
        transaction = Transaction.objects.filter(pk=pk).first()
        product = Product.objects.filter(
            pk=transaction.product_id_id, create_by=user.pk
        ).first()
        if product:
            if product.quantity > transaction.quantity:
                product.quantity = product.quantity - transaction.quantity
                transaction.status = "DONE"
                product.save()
                transaction.save()
                return Response({"message": "OK"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loi"}, status=status.HTTP_400_BAD_REQUEST)
