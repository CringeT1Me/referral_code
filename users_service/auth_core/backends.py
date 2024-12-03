from django.contrib.auth import get_user_model
from django.contrib.auth.backends import AllowAllUsersModelBackend


class AuthBackend(AllowAllUsersModelBackend):
    """
    Возвращает существующего или нового пользователя при аутентификации.
    """

    def authenticate(self, request, phone_number=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            user = UserModel.objects.create_user(phone_number=phone_number)
        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None