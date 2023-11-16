from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentView

router = DefaultRouter()
router.register(r"", CommentView, basename="growup")

urlpatterns = [
    path("/", include(router.urls)),
]
