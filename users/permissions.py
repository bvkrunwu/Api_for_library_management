from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.

    Разрешение предоставляется пользователям, которые входят в группу «moders».
    Используется для ограничения доступа к определённым действиям или эндпоинтам.
    """

    def has_permission(self, request, view):
        """
        Проверяет наличие разрешения на уровне запроса (без привязки к объекту).

        Определяет, принадлежит ли текущий пользователь к группе модераторов.

        Args:
            request (Request): HTTP‑запрос, содержащий информацию о пользователе.
            view (View): Представление (view), к которому обращается пользователь.

        Returns:
            bool: True, если пользователь входит в группу «moders», иначе False.
        """

        return request.user.groups.filter(name="moders").exists()
