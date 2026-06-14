from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserCustomManager(BaseUserManager):
    """
    Кастомный менеджер для модели User.

    Предоставляет методы для создания обычных пользователей и суперпользователей
    с валидацией обязательных полей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет пользователя с email и паролем.

            Выполняет валидацию обязательных полей, нормализует email,
            устанавливает пароль и сохраняет пользователя в базе данных.

            Args:
                email (str): Адрес электронной почты пользователя.
                password (str, optional): Пароль пользователя. По умолчанию None.
                **extra_fields: Дополнительные поля для модели пользователя.

            Raises:
                ValueError: Если email или пароль не указаны.

            Returns:
                User: Созданный экземпляр пользователя.
        """

        if not email:
            raise ValueError("Поле электронной почты должно быть заполнено.")
        if not password:
            raise ValueError("Пароль должен быть указан.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создаёт суперпользователя с повышенными правами.

            Устанавливает обязательные флаги для суперпользователя (is_staff, is_superuser, is_active)
            и вызывает create_user для фактического создания записи.

            Args:
                email (str): Адрес электронной почты суперпользователя.
                password (str): Пароль суперпользователя.
                **extra_fields: Дополнительные поля для модели суперпользователя.

            Raises:
                ValueError: Если пароль не указан или если флаги is_staff/is_superuser
                    не установлены в True.

            Returns:
                User: Созданный экземпляр суперпользователя.
        """

        if not password:
            raise ValueError("Суперпользователь должен иметь пароль.")

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.

    Использует email в качестве основного идентификатора вместо username.
    Включает поля для контактной информации, аватара и флагов доступа.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone_number = models.CharField(
        max_length=35, verbose_name="Номер телефона", blank=True, null=True, help_text="Введите номер телефона"
    )
    country = models.CharField(
        max_length=100, verbose_name="Страна", blank=True, null=True, help_text="Укажите страну"
    )

    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True, help_text="Загрузите аватар"
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserCustomManager()

    class Meta:
        """
        Мета‑опции для модели User.

            Задаёт человеко‑читаемые названия модели в единственном
            и множественном числе для отображения в админ‑панели.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

            Используется в админке Django и других интерфейсах для отображения объекта.

            Returns:
                str: Адрес электронной почты пользователя.
        """

        return self.email
