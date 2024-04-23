from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    If user is an administrator or a superuser then this permission should be allowed
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            (request.user.is_superuser or request.user.is_staff)
        )
