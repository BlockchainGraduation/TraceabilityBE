from django.shortcuts import render
from rest_framework import generics, views, response, status
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import NotificationSerializer
from .models import Notification


# Create your views here.


class NotificationMeViews(views.APIView):
    @swagger_auto_schema(
        tags=["notification"],
        operation_summary="Get notification me",
    )
    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(create_by=request.user.id)
        return response.Response(
            {"detail": NotificationSerializer(notifications, many=True).data},
            status=status.HTTP_200_OK,
        )
