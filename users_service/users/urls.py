from rest_framework.routers import SimpleRouter

from users.views import HTMLUserViewSet, APIUserViewSet

users_router = SimpleRouter()
users_router.register(r'users', HTMLUserViewSet, basename='users')
users_router.register(r'api/v1/users', APIUserViewSet, basename='api-users')

users_urlpatterns = users_router.urls
