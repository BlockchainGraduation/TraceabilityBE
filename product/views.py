from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ProductSerializers
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


# Create your views here.
class ProductViews(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    # permission_classes = [IsOwner]
    # def create(self, request, *args, **kwargs):
    #     image = Image.objects.create(request.FILES)
    #     return super().create(request, *args, **kwargs)

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
