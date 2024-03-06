from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users import views as user_views

router_api_v1 = routers.DefaultRouter()

router_api_v1.register(
    'users',
    user_views.UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),


]
