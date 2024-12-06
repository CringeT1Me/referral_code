from django.contrib.auth import views
from django.urls import path
from rest_framework.routers import SimpleRouter

from auth_core.admin import admin_site
from auth_core.views import APILoginView, LoginView, home_redirect

auth_router = SimpleRouter()
auth_router.register(r'api/v1', APILoginView, basename='api-login')

auth_urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin_site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
auth_urlpatterns += auth_router.urls
