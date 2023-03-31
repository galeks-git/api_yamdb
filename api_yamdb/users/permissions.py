from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Доступ только aдмину."""

    def has_permission(self, request, view):
        return (request.user.is_admin or request.user.is_superuser)
