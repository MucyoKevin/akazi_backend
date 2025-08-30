from django.urls import path
from . import views

urlpatterns = [
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('', views.PaymentListView.as_view(), name='payment_list'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
]
