from rest_framework.permissions import BasePermission


class StaffOnlyPermission(BasePermission):
    """
    Разрешение, которое позволяет доступ только сотрудникам библиотеки.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
