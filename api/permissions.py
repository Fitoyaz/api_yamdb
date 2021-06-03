from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        else:
            return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.role == 'moderator'
            or request.user.role == 'admin'
            or request.user.is_superuser
        ):
            return True
        else:
            return False
