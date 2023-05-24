from rest_framework import permissions


class IsAuthorAdminOrReadOnly(permissions.BasePermission):

    message = 'Неавторизованным пользователям разрешён только просмотр. \
               Если пользователь является администратором \
               или владельцем записи, то возможны остальные методы.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.author == request.user
                or request.user.is_staff
                or request.user.is_admin))
