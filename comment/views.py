from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Comment
from .serializers import CommentSerializers, DetailCommentSerializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# Create your views here.
class IsOwnerComment(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs["pk"]
        superuser = request.user.is_superuser
        comment = Comment.objects.filter(pk=pk, user_id=request.user.id).first()
        return True if comment or superuser else False


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def get_permissions(self):
        if (
            self.action == "partial_update"
            or self.action == "destroy"
            or self.action == "update"
        ):
            return [IsOwnerComment(), permissions.IsAuthenticated()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class GetFilterCommentView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product_id"]
    # search_fields = ["product_id", "user_id"]
    queryset = Comment.objects.all()
    serializer_class = DetailCommentSerializers

    @swagger_auto_schema(
        tags=["comment"],
        operation_summary="Filter Comment",
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                in_=openapi.IN_QUERY,
                description="Lọc theo product",
                type=openapi.TYPE_INTEGER,
            ),
            # openapi.Parameter(
            #     "user_id",
            #     in_=openapi.IN_QUERY,
            #     description="Lọc theo user",
            #     type=openapi.TYPE_INTEGER,
            # ),
            # Các tham số khác nếu cần
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
