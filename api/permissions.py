from rest_framework import permissions

from .models import UserRole


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
             return True
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (
                request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user.is_superuser
            ):
                return True
        return False


class ReviewOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS
                    or obj.author == request.user
                    or request.user.role == UserRole.MODERATOR)
