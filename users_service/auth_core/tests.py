from django.contrib.auth import get_user_model
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


class APILoginViewTest(APITestCase):
    def setUp(self):
        self.phone_number = '89371112004'
        phone_number_obj = PhoneNumber.from_string(phone_number='89371112004')
        self.user = User.objects.create_user(phone_number=phone_number_obj)

    def test_api_login_success(self):
        response = self.client.post('/api/v1/login/', {'phone_number': self.phone_number})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
