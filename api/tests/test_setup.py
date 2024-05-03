from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):

    def setUp(self):
        self.test_url = reverse("test")
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()