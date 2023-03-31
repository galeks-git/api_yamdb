from rest_framework import permissions

MSG_USR_NO_RIGHTS = 'Пользователю не хватает прав для выполнения операции.'


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = MSG_USR_NO_RIGHTS

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# class IsUserOrReadOnly(permissions.BasePermission):
#     message = MSG_USR_NO_RIGHTS

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.user == request.user

# from rest_framework import permissions


# class IsAuthorOrReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if (request.method in permissions.SAFE_METHODS
#             or obj.author == request.user
#             ):
#             return True
