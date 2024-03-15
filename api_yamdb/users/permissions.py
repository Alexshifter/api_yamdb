from rest_framework import permissions


class IsAnonymReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'user')


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsOwnerIsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user) or (
            request.user.is_authenticated
            and (request.user.role in ('moderator', 'admin',))
        ) or (request.method in permissions.SAFE_METHODS)
