from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from users.serializers import UserSerializer


class PhoneLoginSerializer(UserSerializer):
    phone_number = PhoneNumberField(write_only=True)
    class Meta(UserSerializer.Meta):
        read_only_fields = UserSerializer.Meta.fields
        fields = UserSerializer.Meta.fields + ['phone_number']

