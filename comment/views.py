from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializers


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
