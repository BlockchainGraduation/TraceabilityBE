from django.urls import include, path
from .views import GrowUpView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", GrowUpView, basename="growup")

urlpatterns = [
    path("/", include(router.urls)),
]
