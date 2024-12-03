import string

from django.contrib.auth.base_user import BaseUserManager

from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field is required')

        referral_code = self.generate_referral_code()

        user = self.model(referral_code=referral_code, phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, **extra_fields)

    def generate_referral_code(self):
        """Генерация уникального реферального кода."""
        while True:
            referral_code = get_random_string(6, allowed_chars=string.ascii_uppercase + string.digits)
            if not self.model.objects.filter(referral_code=referral_code).exists():
                break
        return referral_code
