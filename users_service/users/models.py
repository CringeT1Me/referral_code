from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import SET_NULL
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    referral_code = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    phone_number = PhoneNumberField(unique=True)
    refers_to = models.ForeignKey(to='self', on_delete=SET_NULL, null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return str(self.phone_number)

