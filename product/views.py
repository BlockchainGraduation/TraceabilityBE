from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProductSerializers
from .models import Product
from user.models import User


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs["pk"]
        # print(view.kwargs["pk"])
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

    def get_permissions(self):
        if (
            self.action == "partial_update"
            or self.action == "delete"
            or self.action == "update"
        ):
            return [IsOwner(), permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]
