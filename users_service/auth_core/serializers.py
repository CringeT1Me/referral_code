from rest_framework import serializers

from users.serializers import UserSerializer


class PhoneLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class CodeVerificationSerializer(UserSerializer):
    code = serializers.CharField(write_only=True)
    class Meta(UserSerializer.Meta):
        read_only_fields = UserSerializer.Meta.fields
        fields = UserSerializer.Meta.fields + ['code']
