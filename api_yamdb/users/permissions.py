from rest_framework import exceptions, permissions, status
from rest_framework.response import Response


class IsAnonymReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'user')


class IsModeratorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'moderator'
        )


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin') or (
            request.method in permissions.SAFE_METHODS
        )

    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'GET':
    #         raise exceptions.MethodNotAllowed(['GET'])
    #     return True
