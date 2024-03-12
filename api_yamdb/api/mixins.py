from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from users.permissions import IsAdminOnly, IsAnonymReadOnly


class CategoryGenreMixinView(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filterset_fields = ('name',)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action == 'list':
            return [IsAnonymReadOnly()]
        return [IsAdminOnly()]
