from random import randint
from django.core.cache import cache

# Добавить Celery
def send_sms_task(phone_number):
    """
    Генерирует OTP код и сохраняет его в кэш на 15 минут.
    На данный момент вместо отправки смс-кода, код выводится в консоль.
    """

    otp_code = randint(1111, 9999)
    cache.set(phone_number, otp_code, timeout=60*5)

    # Имитация отправки сообщения
    print(f'СМС-КОД: {cache.get(phone_number)}')
    # send_sms()
