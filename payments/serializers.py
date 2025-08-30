from rest_framework import serializers
from .models import Wallet, Payment, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'payment_method', 'status', 
            'transaction_id', 'mobile_number', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'transaction_id', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'description', 
            'reference_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
