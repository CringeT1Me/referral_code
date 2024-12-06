from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from auth_core.urls import auth_urlpatterns
from users.urls import users_urlpatterns

schema_view = get_schema_view(
   openapi.Info(
      title='API пользователя.',
      default_version='v1',
      description='API для авторизации, профиля, проверки и применения реферального кода.',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='email@email.com'),
      license=openapi.License(name='Лицензия'),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += users_urlpatterns
urlpatterns += auth_urlpatterns
