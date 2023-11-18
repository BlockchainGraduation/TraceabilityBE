from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Cart
from .serializers import CartSerializers

# Create your views here.


class CartView(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

    def get_permissions(self):
        if (
            self.action == "create"
            or self.action == "partial_update"
            or self.action == "update"
            or self.action == "destroy"
        ):
            return [permissions.IsAuthenticated]
        return [permissions.AllowAny]
