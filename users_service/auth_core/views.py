from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from phonenumber_field.phonenumber import PhoneNumber

from auth_core.forms import PhoneLoginForm
from auth_core.serializers import PhoneLoginSerializer
from users.serializers import UserSerializer


class LoginView(View):
    """
    Форма логина.
    """
    template_name = 'registration/login.html'

    def get(self, request):
        form = PhoneLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhoneLoginForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            phone_number_obj = PhoneNumber.from_string(phone_number=str(phone_number.national_number))
            user = authenticate(phone_number=phone_number_obj)
            login(request, user)
            return redirect(f'/users/{user.pk}')

        return render(request, self.template_name, {'form': form})

class APILoginView(GenericViewSet):
    """
    API для логина и выхода из системы.
    """
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'login':
            return PhoneLoginSerializer
        return serializers.Serializer

    @swagger_auto_schema(
        operation_summary='Вход в систему по номеру телефона.',
        operation_description='Вход без подтверждения номера телефона.',
        request_body=PhoneLoginSerializer,
        responses={
            200: openapi.Response('Успешный вход.', UserSerializer),
            400: 'Ошибка валидации данных.'}
    )
    @action(['post'], detail=False, url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            print(phone_number)
            phone_number_obj = PhoneNumber.from_string(phone_number=str(phone_number))
            user = authenticate(phone_number=phone_number_obj)
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Выйти из системы.',
        operation_description='Завершает текущую сессию пользователя.',
        request_body=no_body,
        responses={200: 'Успешный выход из системы.'},
    )
    @action(['post'], detail=False, url_path='logout')
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

def home_redirect(request):
    return redirect('login')