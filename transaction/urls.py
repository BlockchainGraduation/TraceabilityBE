from django.urls import include, path
from .views import TransactionView, AcceptTransactionView

urlpatterns = [
    path("transaction", TransactionView.as_view()),
    path("accept-transaction/<int:pk>", AcceptTransactionView.as_view()),
]
