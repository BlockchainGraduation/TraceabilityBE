from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path("notification-me", views.NotificationMeViews.as_view()),
    path("delete-notification/<int:pk>", views.DeleteNotificationViews.as_view()),
    path("active-notification/<int:pk>", views.ActiveNotificationViews.as_view()),
]
