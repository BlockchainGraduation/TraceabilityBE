from django.urls import include, path
from .views import (
    TransactionView,
    ChangeStatusTransactionView,
    RetrieveTransactionView,
    FilterTransactionViews,
    CreateMultiTransactionViews,
    TransactionMeView,
)

urlpatterns = [
    path("transaction", TransactionView.as_view()),
    path("get-transaction/<int:pk>", RetrieveTransactionView.as_view()),
    path("transaction-me", TransactionMeView.as_view()),
    path("filter-transaction", FilterTransactionViews.as_view()),
    path("create-multi-transaction", CreateMultiTransactionViews.as_view()),
    path("accept-transaction/<int:pk>", ChangeStatusTransactionView.as_view()),
]
