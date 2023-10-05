from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Transaction
from .serializers import TransactionSerializer
from product.models import Product
from user.models import User

# Create your views here.

from rest_framework import generics


class TransactionView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = ["create_by"]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # super().create(request, *args, **kwargs)

        product = Product.objects.filter(pk=request.data["product_id"]).first()
        if product:
            if product.quantity <= request.data["product_id"]:
                return super().create(request, *args, **kwargs)
        return Response({"message": "Loi"}, status=status.HTTP_400_BAD_REQUEST)


class AcceptTransactionView(APIView):
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
