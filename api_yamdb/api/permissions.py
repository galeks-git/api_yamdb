from rest_framework import permissions

MSG_USR_NO_RIGHTS = 'Пользователю не хватает прав для выполнения операции.'


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = MSG_USR_NO_RIGHTS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """SuperUser django и Админ могут делать CREATE PATCH DELETE запросы """
    message = MSG_USR_NO_RIGHTS

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    message = MSG_USR_NO_RIGHTS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )
