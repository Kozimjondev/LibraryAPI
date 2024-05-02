from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrAdmin(BasePermission):
    """
    Allows access only to authenticated users or admin users.
    """

    def has_object_permission(self, request, view, obj):
        return bool((request.user and request.user.is_authenticated) or request.user.is_superuser or
                    request.user.is_staff)
