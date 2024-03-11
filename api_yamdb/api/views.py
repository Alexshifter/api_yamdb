from django.shortcuts import get_object_or_404
from rest_framework import (
    filters, mixins, permissions, viewsets
)
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrOnlyReadPermission
from api.serializers import (
    CommentSerializer, CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title 


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrOnlyReadPermission,
    )

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrOnlyReadPermission,
    )

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorOrOnlyReadPermission,)
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthorOrOnlyReadPermission,
    )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'

    def get_category(self):
        return Category.objects.get(pk=self.kwargs.get('slug'))
