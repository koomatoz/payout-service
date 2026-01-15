from decimal import Decimal
from rest_framework import serializers
from .models import Payout

def validate_positive_amount(value):
    if value <= 0:
        raise serializers.ValidationError('Amount must be positive.')
    return value

class PayoutSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=18, decimal_places=2, validators=[validate_positive_amount])
    is_terminal = serializers.SerializerMethodField()

    class Meta:
        model = Payout
        fields = ['id', 'amount', 'currency', 'recipient_name', 'recipient_account', 'recipient_bank_code',
                  'status', 'description', 'processed_at', 'failure_reason', 'is_terminal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'processed_at', 'failure_reason', 'is_terminal', 'created_at', 'updated_at']

    def get_is_terminal(self, obj):
        return obj.is_terminal

class PayoutCreateSerializer(PayoutSerializer):
    class Meta(PayoutSerializer.Meta):
        fields = ['id', 'amount', 'currency', 'recipient_name', 'recipient_account', 'recipient_bank_code',
                  'description', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
