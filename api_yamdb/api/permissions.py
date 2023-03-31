from rest_framework import permissions

MSG_USR_NO_RIGHTS = 'Пользователю не хватает прав для выполнения операции.'

class IsAuthorOrReadOnly(permissions.BasePermission):
    message = MSG_USR_NO_RIGHTS

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsSuperUserIsAdminIsAnonim(permissions.BasePermission):
    """SuperUser django и Админ могут делать CREATE PATCH DELETE запросы """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            and request.user.is_admin)
