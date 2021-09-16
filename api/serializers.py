from rest_framework import serializers

from api.models import Order, Stock
from api.services import TradeService


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("name", "price")


class OrderSerializer(serializers.Serializer):

    stock_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)
    action = serializers.CharField(required=True, max_length=100)

    def validate_action(self, value):
        if value not in ("buy", "sell"):
            raise serializers.ValidationError("Invalid action for order")
        return value
