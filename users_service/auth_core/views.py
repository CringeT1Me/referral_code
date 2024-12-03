from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
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
from auth_core.serializers import PhoneLoginSerializer, CodeVerificationSerializer
from auth_core.tasks import send_sms_task
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

            send_sms_task(phone_number.national_number)

            request.session['phone_number'] = phone_number.national_number
            return redirect('verify')

        return render(request, self.template_name, {'form': form})


class CodeVerificationView(View):
    """
    Форма верификации кода.
    """
    template_name = 'registration/verify.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.session.get('phone_number')
        if not phone_number:
            return redirect('login')

        entered_code = request.POST.get('code')
        stored_code = cache.get(phone_number)

        if str(stored_code) == entered_code:
            phone_number_obj = PhoneNumber.from_string(phone_number=str(phone_number))
            user = authenticate(phone_number=phone_number_obj)
            login(request, user)
            return redirect(f'/users/{user.pk}')
        else:
            return render(request, self.template_name, {'error': 'Неправильный код подтверждения.'}, status=400)

class APILoginView(GenericViewSet):
    """
    API для логина, верификации кода и выхода из системы.
    """
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'login':
            return PhoneLoginSerializer
        elif self.action == 'verify':
            return CodeVerificationSerializer
        return serializers.Serializer

    @swagger_auto_schema(
        operation_summary='Вход в систему по номеру телефона.',
        operation_description='Отправка SMS с кодом подтверждения на указанный номер телефона.',
        request_body=PhoneLoginSerializer,
        responses={200: openapi.Response('Код отправлен'), 400: 'Ошибка валидации данных.'}
    )
    @action(['post'], detail=False, url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            send_sms_task(phone_number)
            request.session['phone_number'] = phone_number
            return Response({'detail': 'Код отправлен.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Ввод кода подтверждения.',
        operation_description='Верификация введенного кода подтверждения.',
        request_body=CodeVerificationSerializer,
        responses={
            200: openapi.Response('Успешный вход.', UserSerializer),
            400: openapi.Response('Неправильный код подтверждения.')
        }
    )
    @action(['post'], detail=False, url_path='verify')
    def verify(self, request):
        phone_number = request.session.get('phone_number')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            entered_code = serializer.validated_data['code']
            stored_code = cache.get(phone_number)
            if str(stored_code) == entered_code:
                phone_number_obj = PhoneNumber.from_string(phone_number=str(phone_number))
                user = authenticate(phone_number=phone_number_obj)
                login(request, user)
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Неправильный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)
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
