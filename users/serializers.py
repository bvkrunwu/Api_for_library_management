from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Базовый сериализатор для модели User.

    Используется для операций со списком пользователей и базовыми данными пользователя,
    включая управление правами доступа (is_staff, is_active).
    """

    class Meta:
        """
        Мета‑опции для UserSerializer.

        Определяет модель и полный набор полей для сериализации пользователя,
        включая идентификационные данные, контактную информацию и флаги доступа.
        """

        model = User
        fields = ["id", "email", "password", "phone_number", "country", "avatar", "is_staff", "is_active"]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля пользователя.

    Включает основную информацию о пользователе.
    Используется для отображения детальной информации о профиле пользователя.
    """

    class Meta:
        """
        Мета‑опции для UserProfileSerializer.

        Определяет модель и набор полей для представления профиля пользователя.
        """

        model = User
        fields = ["email", "phone_number", "country", "avatar"]
