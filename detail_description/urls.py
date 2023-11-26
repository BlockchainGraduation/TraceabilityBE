from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"detai_description",
    views.DetailDescriptionView,
    basename="detai_description",
)

urlpatterns = [
    path("", include(router.urls)),
]
