from pydoc import pager

from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.management.commands.drf_create_token import UserModel
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serializers import UserSerializer, ReferralCodeSerializer


class BaseUserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """
    Базовый класс для наследования.
    API для валидации и применения реферального кода,
    а также получения списка профилей и конкретного профиля.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    UserModel = get_user_model()
    queryset = UserModel.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    @swagger_auto_schema(
        operation_summary='Получить профиль пользователя.',
        operation_description='Возвращает профиль конкретного пользователя по его ID.',
        responses={
            200: openapi.Response('Детали пользователя.', UserSerializer),
            403: openapi.Response('Пользователь не авторизован.'),
            404: openapi.Response('Пользователь не найден.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Переопределение retrieve для добавления документации"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Получить список пользователей.',
        operation_description='Возвращает список пользователей в пределах пагинации.',
        responses={
            200: openapi.Response('Список пользователей.', UserSerializer(many=True)),
            403: openapi.Response('Пользователь не авторизован.'),
            404: openapi.Response('Страница пуста')
        }
    )
    def list(self, request, *args, **kwargs):
        """Переопределение list для добавления документации"""
        return super().list(request, *args, **kwargs)

class APIUserViewSet(BaseUserViewSet):
    """
    API для валидации и применения реферального кода,
    а также получения списка профилей и конкретного профиля.
    """

    def get_serializer_class(self):
        if self.action == "apply_referral":
            return ReferralCodeSerializer
        return UserSerializer

    @swagger_auto_schema(
        operation_summary='Применить реферальный код.',
        operation_description='Позволяет пользователю активировать реферальный код.',
        request_body=ReferralCodeSerializer,
        responses={
            200: openapi.Response('Успешное применение кода.', UserSerializer),
            400: openapi.Response('Ошибка валидации.'),
            403: openapi.Response('Пользователь не авторизован.')
        }
    )
    @action(['post'], detail=False, url_path='apply-referral')
    def apply_referral(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        referred_user = serializer.validated_data['referral_code']
        user = self.request.user
        user.refers_to = referred_user
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Валидировать реферальный код.',
        operation_description='Проверяет, доступен ли указанный реферальный код.',
        manual_parameters=[
            openapi.Parameter(
                'referral_code',
                openapi.IN_PATH,
                description='Реферальный код для проверки.',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Код доступен.'),
            400: openapi.Response('Ошибка: неверный код или код уже активирован.'),
            403: openapi.Response('Пользователь не авторизован.')
        }
    )
    @action(['get'], detail=False, url_path=r'validate-referral/(?P<referral_code>[^/.]+)')
    def validate_referral(self, request, referral_code=None):
        if self.request.user.refers_to:
            return Response({'detail': 'Вы уже активировали код.'}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user.referral_code == referral_code:
            return Response({'detail': 'Нельзя активировать собственный код.'}, status=status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(referral_code=referral_code).exists():
            return Response({'detail': 'Код доступен.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)

class HTMLUserViewSet(BaseUserViewSet):
    """
    Форма для профиля и списка профилей.
    """
    renderer_classes = [TemplateHTMLRenderer]

    def get_template_names(self):
        if self.action == 'list':
            return ['profile/list.html']
        return ['profile/retrieve.html']

