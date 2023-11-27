from django.shortcuts import render
from rest_framework import generics, views, response, status
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import NotificationSerializer, DeleteNotificationSerializer
from .models import Notification


# Create your views here.


class NotificationMeViews(views.APIView):
    @swagger_auto_schema(
        tags=["notification"],
        operation_summary="Get notification me",
    )
    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(create_by=request.user.id).order_by(
            "-create_at"
        )
        unread = Notification.objects.filter(
            create_by=request.user.id, active=False
        ).count()
        return response.Response(
            {
                "detail": NotificationSerializer(notifications, many=True).data,
                "unread": unread,
            },
            status=status.HTTP_200_OK,
        )


class DeleteNotificationViews(views.APIView):
    def delete(self, request, *args, **kwargs):
        Notification.objects.filter(
            create_by=request.user.id, pk=kwargs["pk"]
        ).first().delete()
        return response.Response(
            {"detail": "SUCCESS"},
            status=status.HTTP_200_OK,
        )


class ActiveNotificationViews(views.APIView):
    def patch(self, request, *args, **kwargs):
        notification = Notification.objects.filter(
            create_by=request.user.id, pk=kwargs["pk"]
        ).first()
        if notification:
            notification.active = True
            notification.save()
            return response.Response(
                {"detail": "SUCCESS"},
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"detail": "NOTIFICATION_NOT_EXISTS"},
                status=status.HTTP_400_BAD_REQUEST,
            )
