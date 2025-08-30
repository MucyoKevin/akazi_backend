from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Wallet, Payment, Transaction
from .serializers import WalletSerializer, PaymentSerializer, TransactionSerializer

class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    
    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')
