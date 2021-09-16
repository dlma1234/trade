import json

from rest_framework.test import (
    APITestCase, 
    APIClient
)
from django.contrib.auth.models import User
from django.urls import reverse

from api.models import Order, Stock
from api.services import TradeService


class TradeAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user", 
            email="test_user@test.com", 
            password="testpass"
        )
        self.stock_foo = self._create_stock(
            name="Foo", price=40
        )

    def test_user_logs_in_success(self):
        response = self.client.login(
            username="test_user", password="testpass"
        )
        self.assertTrue(response)

    def test_user_logs_in_failed(self):
        response = self.client.login(
            username="test_user", password="testpass-xxxxx"
        )
        self.assertFalse(response)
    
    def test_post_order_buy(self):
        self.client.force_authenticate(user=self.user)

        stock_to_buy = self.stock_foo
        
        path = reverse("order_view")
        user_input = {
            "stock_id": stock_to_buy.id,
            "quantity": 20,
            "action": "buy"
        }

        response = self.client.post(
            path=path, data=user_input, format="json"
        )

        self.assertEqual(response.status_code, 201)

        order_exists = Order.objects.filter(
            user_id=self.user.id,
            stock_id=stock_to_buy.id, 
            action="buy", 
            quantity=20, 
            total=800,
        ).exists()

        self.assertTrue(order_exists)

    def test_post_order_sell(self):
        self.client.force_authenticate(user=self.user)

        stock_to_sell = self.stock_foo
        
        path = reverse("order_view")
        user_input = {
            "stock_id": stock_to_sell.id,
            "quantity": 50,
            "action": "sell"
        }

        response = self.client.post(
            path=path, data=user_input, format="json"
        )

        self.assertEqual(response.status_code, 201)

        sell_order_exists = Order.objects.filter(
            user_id=self.user.id,
            stock_id=stock_to_sell.id, 
            action="sell", 
            quantity=50, 
            total=-2000,
        ).exists()

        self.assertTrue(sell_order_exists)

    def test_get_stock_by_name(self):
        self.client.force_authenticate(user=self.user)
        
        # url = "/stocks/?name=foo"
        url = reverse("stock_view") + "?name=Foo"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.content, encoding='utf8'), 
            '{"name": "Foo", "price": "40.00"}'
        )

    def test_get_total_value_by_user_and_stock(self):
        self.client.force_authenticate(user=self.user)

        # Create another stock named "Bar"
        stock_bar = self._create_stock(name="Bar", price=50)

        # Create 2 orders for stock Foo
        self._create_order(stock_id=self.stock_foo.id, quantity=100, action="buy") # +4000
        self._create_order(stock_id=self.stock_foo.id, quantity=20, action="sell") # -800

        # Create an order for stock Bar
        self._create_order(stock_id=stock_bar.id, quantity=50, action="buy") # + 2500

        url = "/user/{user_id}/stock/{stock_id}/total".format(
            user_id=self.user.id, 
            stock_id=self.stock_foo.id
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.content, encoding='utf8'), 
            '{"total": "3200.00"}'
        )

        # Test the value for stock Bar
        url = "/user/{user_id}/stock/{stock_id}/total".format(
            user_id=self.user.id, 
            stock_id=stock_bar.id
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.content, encoding='utf8'), 
            '{"total": "2500.00"}'
        )
        
    # Helper methods
    def _create_stock(self, name, price):
        stock = Stock(name=name, price=price)
        stock.save()
        return stock

    def _create_order(self, stock_id, quantity, action):
        order = TradeService().create_order(
            user=self.user, stock_id=stock_id, quantity=quantity, action=action
        )
