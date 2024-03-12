from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from users.permissions import IsAdminOnly


class CategoryGenreMixinView(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOnly,)
    search_fields = ('name',)
