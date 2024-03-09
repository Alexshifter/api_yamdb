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
    path(
        'v1/auth/signup/', user_views.UserRegView.as_view({'post': 'create'})
    ),
    path('v1/auth/token/', user_views.UserTokenView.as_view()),
]
