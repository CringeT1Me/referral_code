from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class ReferralPhoneSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['phone_number']

class UserSerializer(ModelSerializer):
    referrals = serializers.SerializerMethodField()
    applied_code  = serializers.CharField(source='refers_to.referral_code', required=False, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'phone_number', 'referral_code', 'referrals', 'refers_to', 'applied_code']
        read_only_fields = fields

    @swagger_serializer_method(serializer_or_field=ReferralPhoneSerializer(many=True))
    def get_referrals(self, obj):
        referred_users = obj.__class__.objects.select_related('refers_to').filter(refers_to=obj)
        return ReferralPhoneSerializer(referred_users, many=True).data

    def validate_phone_number(self, value):
        try:
            validate_international_phonenumber(value)
        except ValidationError:
            raise ValidationError('Некорректный номер телефона.')
        return value

class ReferralCodeSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['referral_code']

    def validate_referral_code(self, value):
        try:
            UserModel = get_user_model()
            referred_user = UserModel.objects.get(referral_code=value)
            request_user = self.context['request'].user
            if referred_user == request_user:
                raise ValidationError('Вы не можете использовать собственный реферальный код.')
        except UserModel.DoesNotExist:
            raise ValidationError('Код не действителен.')
        return referred_user
