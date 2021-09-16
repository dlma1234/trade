import json

from rest_framework.test import (
    APITestCase, 
    APIClient
)
from django.contrib.auth.models import User


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

# Create your tests here.
