from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LongestIncreasingPathAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("longest-increasing-path")

    def test_kth_largest(self):
        payload = {"matrix": [[9, 9, 4], [6, 6, 8], [2, 1, 1]]}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"result": 4})
