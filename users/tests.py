from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User, Subscription, UserNotificationSettings
from users import views

class AuthenticationTests(APITestCase):
    def setUp(self):
        User.objects.create_user(email='test@example.com', password='testpassword')
        self.create_account_url = reverse('create-account')

    def test_create_user(self):
        data = {'email': 'test2@example.com', 'password': 'testpassword'}
        response = self.client.post(self.create_account_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_create_duplicate_user(self):
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.create_account_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        url = reverse('login')

        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class PersonalInfoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_get_personal_info(self):
        url = reverse('personal-info')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SignupPaymentInfoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.signup_payment_url = reverse('signup-payment-info')

    def test_signup_payment_info_success(self):
        data = {
            'period': 0,
            'plan': 0,
            'currency': 'EUR',
            'card_info': '123'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.signup_payment_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_payment_info_failure(self):
        data = {
            'card_info': '123'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.signup_payment_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.change_password_url = reverse('change-password')

    def test_change_password_success(self):
        data = {
            'old_password': 'testpassword',
            'password': 'newtestpassword',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.change_password_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Password changed successfully')

    def test_change_password_invalid_old_password(self):
        data = {
            'old_password': 'wrongoldpassword',
            'password': 'newtestpassword',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.change_password_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid old password')

    def test_change_password_missing_data(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.change_password_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SubscriptionInfoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.subscription_info_url = reverse('subscription-info')

    def test_get_subscription_info_success(self):
        Subscription.objects.create(user=self.user, plan=0, is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.subscription_info_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.logout_url = reverse('logout')

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PaymentInfoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.payment_info_url = reverse('payment-info')

    def test_get_payment_info_success(self):
        self.user.location = 'NY'
        self.user.currency = 'USD'
        self.user.card_info = '123'
        self.user.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.payment_info_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_payment_info_failure(self):
        response = self.client.get(self.payment_info_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_payment_info_success(self):
        data = {
            'location': 'EME',
            'currency': 'EUR',
            'card_info': '123',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.payment_info_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_payment_info_failure(self):
        data = {
            'location': 'EME',
            'card_info': '123',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.payment_info_url, data, format='json')

        self.assertEqual(response.status_code, 400)

class LocalizationInfoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.localization_info_url = reverse('localization-info')

    def test_get_localization_info_success(self):
        self.user.language = 'EN'
        self.user.timezone = '0'
        self.user.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.localization_info_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_localization_info_failure(self):
        response = self.client.get(self.localization_info_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_localization_info_success(self):
        data = {
            'language': 'EN',
            'timezone': '0',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.localization_info_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_localization_info_failure(self):
        data = {
            'language': 'RU',
            'timezone': '4',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.localization_info_url, data, format='json')

        self.assertEqual(response.status_code, 400)

class NotificationSettingsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.notification_settings_url = reverse('notification-settings')

    def test_get_notification_settings_success(self):
        UserNotificationSettings.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.notification_settings_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_settings_failure(self):
        response = self.client.get(self.notification_settings_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_notification_settings_success(self):
        data = {
            'new_predictions': False,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.notification_settings_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)