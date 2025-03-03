from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class KthLargestAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("kth-largest")

    def test_kth_largest(self):
        payload = {"nums": [3, 2, 1, 5, 6, 4], "k": 2}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"result": 5})
