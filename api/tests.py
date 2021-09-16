import json

from rest_framework.test import (
    APITestCase, 
    APIClient
)
from django.contrib.auth.models import User

from api.models import Order, Stock


class TradeAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_logs_in_success(self):
        user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="testpass"
        )

        response = self.client.login(username="test_user", password="testpass")
        self.assertTrue(response)

    def test_user_logs_in_failed(self):
        user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="testpass"
        )

        response = self.client.login(username="test_user", password="testpass-xxxxx")
        self.assertFalse(response)
    
    def test_post_order_buy(self):
        stock_to_buy = self._create_stock(name="Foo", price=40)
        
        path = "/orders"
        user_input = {
            "stock_id": stock_to_buy.id,
            "quantity": 20,
            "action": "buy"
        }

        response = self.client.post(path=path, data=user_input)

        expected_order = Order.objects.get(stock_id=stock_to_buy.id, action="buy")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(expected_order), 1)
        self.assertEqual(expected_order.quantity, 20)
        self.assertEqual(expected_order.total, 800)

    # Helper methods
    def _create_stock(self, name, price):
        stock = Stock(name=name, price=price)
        stock.save()
        return stock
