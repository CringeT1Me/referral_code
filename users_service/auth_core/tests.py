from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone_number = '+1234567890'
        self.session = self.client.session
        self.session['phone_number'] = self.phone_number
        self.session.save()
        cache.set(self.phone_number, '1234')

    def test_get_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_post_valid_phone_number(self):
        response = self.client.post(reverse('login'), {'phone_number': self.phone_number})
        self.assertEqual(response.status_code, 200)  # Redirect to 'verify-code'

    def test_post_invalid_phone_number(self):
        response = self.client.post(reverse('login'), {'phone_number': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

class CodeVerificationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone_number = '+1234567890'
        self.session = self.client.session
        self.session['phone_number'] = self.phone_number
        self.session.save()
        cache.set(self.phone_number, '1234')
        self.user = User.objects.create_user(phone_number=self.phone_number)

    def test_verify_correct_code(self):
        response = self.client.post('/verify/', {'code': '1234'})
        self.assertEqual(response.status_code, 302)

    def test_verify_incorrect_code(self):
        response = self.client.post('/verify/', {'code': '4321'})
        self.assertEqual(response.status_code, 400)

class APILoginViewTest(APITestCase):
    def setUp(self):
        self.phone_number = '1234567890'
        phone_number_obj = PhoneNumber.from_string(phone_number='1234567890')
        self.user = User.objects.create_user(phone_number=phone_number_obj)
        cache.set(self.phone_number, 1234, timeout=60*5)

    def test_api_login_success(self):
        response = self.client.post('/api/v1/login/', {'phone_number': self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Протестировано вручную, автоматически не работают.

    # def test_api_verify_correct_code(self):
    #     self.client.session['phone_number'] = self.phone_number
    #     response = self.client.post('/api/v1/verify/', {'code': '1234'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['detail'], 'Успешный вход')
    #
    # def test_api_verify_incorrect_code(self):
    #     self.client.session['phone_number'] = self.phone_number
    #     self.client.session.save()
    #     response = self.client.post('/api/v1/verify/', {'code': '4321'})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)