from django.db import models

from config import settings


class Author(models.Model):
    """
    Модель для хранения информации об авторах книг.

    Содержит персональные данные автора и даты рождения/смерти.
    Отображается в админ-панели отсортированной по фамилии и имени.
    """

    first_name = models.CharField(max_length=100, verbose_name="Имя", help_text="Введите имя автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", help_text="Введите фамилию автора")
    date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True,
        help_text="Укажите дату рождения автора",
    )
    date_of_death = models.DateField(
        verbose_name="Дата смерти", null=True, blank=True, help_text="Укажите дату смерти автора (если применимо)"
    )

    class Meta:
        """
        Метаданные модели Author.

        Определяют порядок сортировки и отображение в админ-панели.
        """

        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        """
        Строковое представление экземпляра Author.

        Возвращает комбинацию фамилии и имени автора.
        """
        return f"{self.last_name}  {self.first_name}"


class Book(models.Model):
    """
    Модель для хранения информации о книгах.

    Содержит основную информацию о книге: название, автора, краткое описание, ISBN и жанр.
    Отображается в админ-панели отсортированной по названию.
    """

    title = models.CharField(max_length=200, verbose_name="Название", help_text="Введите название книги")
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, verbose_name="Автор", null=True, help_text="Выберите автора книги"
    )
    summary = models.TextField(
        max_length=1000, verbose_name="Краткое описание", help_text="Введите краткое описание книги"
    )
    isbn = models.CharField(
        max_length=13, unique=True, verbose_name="ISBN", help_text="Введите уникальный ISBN-код книги"
    )
    genre = models.ManyToManyField("Genre", verbose_name="Жанры", help_text="Выберите жанр(-ы) для этой книги")

    class Meta:
        """
        Метаданные модели Book.

        Определяют порядок сортировки и отображение в админ-панели.
        """

        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["title"]

    def __str__(self):
        """
        Строковое представление экземпляра Book.

        Возвращает название книги.
        """
        return self.title


class Genre(models.Model):
    """
    Модель для хранения информации о жанрах книг.

    Предназначена для классификации книг по литературным направлениям.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Название жанра",
        help_text="Введите название жанра книги (например, Научная фантастика)",
    )

    class Meta:
        """
        Метаданные модели Genre.

        Определяют отображение в админ-панели.
        """

        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        """
        Строковое представление экземпляра Genre.

        Возвращает название жанра.
        """
        return self.name


class BookCheckout(models.Model):
    """
    Модель для учета выдачи книг пользователям.

    Хранит информацию о выданных книгах, датах выдачи и возврата, статусе возврата.
    Обеспечивает уникальные комбинации пользователя, книги и статуса возврата.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя, взявшего книгу",
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name="Книга", help_text="Выберите книгу, взятую пользователем"
    )
    checkout_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата выдачи", help_text="Дата, когда книга была выдана пользователю"
    )
    due_date = models.DateTimeField(verbose_name="Срок возврата", help_text="Предполагаемая дата возврата книги")
    return_date = models.DateTimeField(
        verbose_name="Фактическая дата возврата",
        blank=True,
        null=True,
        help_text="Дата фактического возврата книги (при возврате)",
    )
    is_returned = models.BooleanField(
        default=False, verbose_name="Возвращена?", help_text="Отметьте, если книга была возвращена"
    )

    class Meta:
        """
        Метаданные модели BookCheckout.

        Определяют отображение в админ-панели и уникальные ограничения.
        """

        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книг"
        unique_together = ("user", "book", "is_returned")

    def __str__(self):
        """
        Строковое представление экземпляра BookCheckout.

        Возвращает информацию о книге, пользователе и статусе возврата.
        """
        return f"{self.book.title} — {self.user.username} ({'возвращена' if self.is_returned else 'не возвращена'})"
