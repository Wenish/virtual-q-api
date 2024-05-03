from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')

        # Sample user data for registration
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if user is actually created
        user_exists = User.objects.filter(username=self.user_data['username']).exists()
        self.assertTrue(user_exists)

    def test_user_registration_invalid_password(self):
        # Invalid password case
        self.user_data['password'] = '1234'  # too short
        self.user_data['password2'] = '1234'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if user is not created
        user_exists = User.objects.filter(username=self.user_data['username']).exists()
        self.assertFalse(user_exists)

    def test_user_registration_passwords_not_matching(self):
        # Passwords not matching case
        self.user_data['password2'] = 'differentpassword'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if user is not created
        user_exists = User.objects.filter(username=self.user_data['username']).exists()
        self.assertFalse(user_exists)