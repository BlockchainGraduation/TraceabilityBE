from django.urls import include, path
from .views import (
    TransactionView,
    ChangeStatusTransactionView,
    RetrieveTransactionView,
    TransactionMeView,
)

urlpatterns = [
    path("transaction", TransactionView.as_view()),
    path("get-transaction/<int:pk>", RetrieveTransactionView.as_view()),
    path("transaction-me", TransactionMeView.as_view()),
    path("accept-transaction/<int:pk>", ChangeStatusTransactionView.as_view()),
]
