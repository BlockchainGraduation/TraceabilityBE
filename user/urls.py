from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenObtainPairView,
)
from . import views

urlpatterns = [
    path(
        "login",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
        kwargs={"tag": "auth"},
    ),
    path("token/refresh", views.MyTokenRefreshView.as_view(), name="token_refresh"),
    path("register", views.RegisterView.as_view()),
    path("forget", views.ForgetView.as_view()),
    path("reset-password", views.ResetPasswordView.as_view()),
    path("confirmOTP", views.ConfirmOTP.as_view()),
    path("survey", views.RegisterRuleView.as_view()),
    path("logout", views.LogoutView.as_view(), name="token_blacklist"),
    path("user", views.UserView.as_view()),
    path("user/me", views.GetMeView.as_view()),
    path("user/statistical", views.StatisticalView.as_view()),
    path("user/update", views.UpdateUserView.as_view()),
    path("user/<uuid:pk>", views.GetUserView.as_view()),
    path("user/list", views.GetListUserView.as_view()),
    path("user/confirm", views.ConfirmUserView.as_view()),
    path("user/lock", views.BlackUserView.as_view()),
]
