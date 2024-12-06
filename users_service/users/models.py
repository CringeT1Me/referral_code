from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import SET_NULL
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    referral_code = models.CharField(verbose_name='Реферальный код', max_length=6, validators=[MinLengthValidator(6)])
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=True)
    refers_to = models.ForeignKey(
        verbose_name='Пользователь, к которому применен реферальный код',
        to='self',
        on_delete=SET_NULL,
        null=True,
        blank=True)

    is_staff = models.BooleanField(verbose_name='Админ', default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'