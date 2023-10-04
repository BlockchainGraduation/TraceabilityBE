from django.urls import include, path
from .views import ProductViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"product", ProductViews, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
