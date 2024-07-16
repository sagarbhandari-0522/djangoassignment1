from django.test import TestCase

# Create your tests here.
# myapp/tests.py
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status

from users.serializers import UserRegisterSerializer


class UserAuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('user_login')
        self.logout_url = reverse('user_logout')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'email': 'testuser@example.com'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_logout(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Successfully logged out')

    def test_valid_serializer(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'email': 'testuser@example.com'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirmation': 'differentpassword',
            'email': 'testuser@example.com'
        }
        serializer = UserRegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_email_already_exists(self):
        # Create a user with the same email first
        User.objects.create_user(username='existinguser', password='testpassword', email='testuser@example.com')

        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'email': 'testuser@example.com'
        }
        serializer = UserRegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_username_already_exists(self):
        # Create a user with the same username first
        User.objects.create_user(username='testuser', password='testpassword', email='existinguser@example.com')

        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'email': 'testuser@example.com'
        }
        serializer = UserRegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
