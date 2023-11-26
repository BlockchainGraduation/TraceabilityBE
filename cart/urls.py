from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"cart", views.CartView, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
    path("cart-me", views.CartMeView.as_view()),
]
