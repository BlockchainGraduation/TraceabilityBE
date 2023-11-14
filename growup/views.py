from django.shortcuts import render
from rest_framework import viewsets, response, status
from drf_yasg.utils import swagger_auto_schema
from .models import GrowUp
from .serializers import GrowUpSerializers
from rest_framework import permissions
from product.views import IsOwnerProduct

# Create your views here.


class GrowUpView(viewsets.ModelViewSet):
    queryset = GrowUp.objects.all()
    serializer_class = GrowUpSerializers

    def get_permissions(self):
        if (
            self.action == "partial_update"
            or self.action == "delete"
            or self.action == "update"
        ):
            return [permissions.IsAuthenticated(), IsOwnerProduct()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return response.Response(
            {"detail": "NOT_ALLOWED"}, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return response.Response(
            {"detail": "NOT_ALLOWED"}, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return response.Response(
            {"detail": "NOT_ALLOWED"}, status=status.HTTP_400_BAD_REQUEST
        )
