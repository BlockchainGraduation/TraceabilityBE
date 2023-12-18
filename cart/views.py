from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializers, DetailCartSerializers


# Create your views here.
class IsOwnerCart(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs["pk"]
        # print(view.kwargs["pk"])
        # print(view.kwargs["pk"])
        # print("user", request.user.id)
        # superuser = request.user.is_superuser
        cart = Cart.objects.filter(pk=pk, create_by=request.user).first()
        return True if cart else False


class CartMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["cart"],
        operation_summary="Cart me",
        # manual_parameters=[
        #     openapi.Parameter(
        #         "status",
        #         in_=openapi.IN_QUERY,
        #         description="Lọc theo status",
        #         type=openapi.TYPE_STRING,
        #     ),
        # ],
    )
    def get(self, request, *args, **kwargs):
        transactions = Cart.objects.filter(create_by=request.user.pk)
        return Response(
            DetailCartSerializers(transactions, many=True).data,
            status=status.HTTP_202_ACCEPTED,
        )


class CartView(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

    def get_permissions(self):
        # if (
        #     self.action == "create"
        #     or self.action == "partial_update"
        #     or self.action == "update"
        #     or self.action == "destroy"
        # ):
        #     return [permissions.IsAuthenticated()]
        if self.action == "destroy":
            return [IsOwnerCart(), permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
