from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Доступ только aдмину."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
