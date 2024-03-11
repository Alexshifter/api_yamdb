from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import CommentViewSet, TitleViewSet, GenreViewSet, CategoryViewSet, ReviewViewSet
from users import views as user_views


api_v1_router = DefaultRouter()
api_v1_router.register('titles', TitleViewSet, basename='titles')
api_v1_router.register('genres', GenreViewSet, basename='genres')
api_v1_router.register('categories', CategoryViewSet, basename='categories')
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', CommentViewSet, basename='comments'
)
api_v1_router.register(
    'users',
    user_views.UserViewSet,
    basename='users')


urlpatterns = [
    path('v1/', include(api_v1_router.urls)),



    path('v1/', include(api_v1_router.urls)),
    path(
        'v1/auth/signup/', user_views.UserRegView.as_view({'post': 'create'})
    ),
    path('v1/auth/token/', user_views.UserTokenView.as_view()),
]
