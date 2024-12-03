from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from users.serializers import UserSerializer


class PhoneLoginSerializer(UserSerializer):
    phone_number = PhoneNumberField()


