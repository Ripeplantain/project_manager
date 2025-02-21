from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class AuthViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.login_url = reverse('auth-login')
        self.logout_url = reverse('auth-logout')
        self.register_url = reverse('auth-register')

    def create_user(self, username='testuser', password='testpass123'):
        return self.User.objects.create_user(username=username, password=password)

    def test_register_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.user_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(self.User.objects.filter(username='testuser').exists())

    def test_register_missing_fields(self):
        """Test registration with missing required fields"""
        response = self.client.post(self.register_url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_duplicate_username(self):
        """Test registration with existing username"""
        # Create user first
        self.create_user()
        
        # Try to create duplicate user
        response = self.client.post(self.register_url, self.user_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Username already exists')

    def test_login_success(self):
        """Test successful login"""
        user = self.create_user()
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post(self.login_url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_logout_success(self):
        """Test successful logout"""
        user = self.create_user()
        refresh = RefreshToken.for_user(user)
        
        response = self.client.post(self.logout_url, {
            'refresh': str(refresh)
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout_missing_token(self):
        """Test logout without refresh token"""
        response = self.client.post(self.logout_url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_logout_invalid_token(self):
        """Test logout with invalid refresh token"""
        response = self.client.post(self.logout_url, {
            'refresh': 'invalid-token'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_with_optional_fields(self):
        """Test registration with only required fields"""
        minimal_data = {
            'username': 'minimaluser',
            'password': 'testpass123'
        }
        response = self.client.post(self.register_url, minimal_data)
        
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        invalid_email_data = self.user_data.copy()
        invalid_email_data['email'] = 'invalid-email'
        
        response = self.client.post(self.register_url, invalid_email_data)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)