import json

from rest_framework.test import (
    APITestCase, 
    APIClient
)
from django.contrib.auth.models import User
from django.urls import reverse

from api.models import Order, Stock


class TradeAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="testpass"
        )

    def test_user_logs_in_success(self):
        response = self.client.login(username="test_user", password="testpass")
        self.assertTrue(response)

    def test_user_logs_in_failed(self):
        response = self.client.login(username="test_user", password="testpass-xxxxx")
        self.assertFalse(response)
    
    def test_post_order_buy(self):
        self.client.force_authenticate(user=self.user)

        stock_to_buy = self._create_stock(name="Foo", price=40)
        
        path = reverse("order_view")
        user_input = {
            "stock_id": stock_to_buy.id,
            "quantity": 20,
            "action": "buy"
        }

        response = self.client.post(path=path, data=user_input, format="json")

        self.assertEqual(response.status_code, 201)

        order_exists = Order.objects.filter(
            user_id=self.user.id,
            stock_id=stock_to_buy.id, 
            action="buy", 
            quantity=20, 
            total=800,
        ).exists()

        self.assertTrue(order_exists)


    # Helper methods
    def _create_stock(self, name, price):
        stock = Stock(name=name, price=price)
        stock.save()
        return stock
