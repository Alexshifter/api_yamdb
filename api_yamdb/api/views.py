from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import (decorators, filters, permissions, viewsets)
from rest_framework.pagination import LimitOffsetPagination

from api.mixins import CategoryGenreMixinView
from api.serializers import (
    CommentSerializer, CategorySerializer, GenreSerializer, GetTitleSerializer, PostPatchTitleSerializer, ReviewSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import IsAuthUserOnly, IsAdminOnly, IsAnonymReadOnly, IsModeratorOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre__slug')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return PostPatchTitleSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class GenreViewSet(CategoryGenreMixinView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filterset_fields = ('name',)
    search_fields = ('name',)


class CategoryViewSet(CategoryGenreMixinView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ('name',)
    search_fields = ('name',)
