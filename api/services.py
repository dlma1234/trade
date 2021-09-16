from decimal import Decimal

from api.models import Order, Stock

class TradeService:

    def create_order(self, user, stock_id, quantity, action):
        stock = Stock.objects.get(id=stock_id)
        total_amount = Decimal(str(quantity)) * stock.price
        order = Order.objects.create(
            user_id=user, 
            quantity=quantity, 
            action=action,
            stock_id=stock, 
            total=total_amount
        )

        return order

