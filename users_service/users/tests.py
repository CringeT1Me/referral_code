from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class ReferralCodeTest(APITestCase):
    def setUp(self):
        phone_number_obj = PhoneNumber.from_string(phone_number='1234567890')
        self.user = User.objects.create_user(phone_number=phone_number_obj)
        phone_number_obj = PhoneNumber.from_string(phone_number='0987654321')
        self.other_user = User.objects.create_user(phone_number=phone_number_obj)
        self.client.force_authenticate(user=self.user)

    def test_apply_valid_referral_code(self):
        response = self.client.post('/api/v1/users/apply-referral/', {'referral_code': self.other_user.referral_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.refers_to, self.other_user)

    def test_apply_invalid_referral_code(self):
        response = self.client.post('/api/v1/users/apply-referral/', {'referral_code': 'INVALID'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_referral_code_success(self):
        response = self.client.get(f'/api/v1/users/validate-referral/{self.other_user.referral_code}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_referral_code_failure(self):
        response = self.client.get('/api/v1/users/validate-referral/INVALID/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
