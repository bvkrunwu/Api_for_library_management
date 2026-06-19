from rest_framework import serializers

from library.models import Author, Book, BookCheckout, Genre


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления авторов книг.

    Преобразует объект Author в формат, подходящий для передачи через API.
    Добавляет дополнительное поле `full_name`, формирующее полное имя автора.

    Attributes:
        full_name (SerializerMethodField): Поле, представляющее полное имя автора.
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        """
        Метаданные сериализатора AuthorSerializer.

        Определяют модель и поля, подлежащие сериализации.
        """

        model = Author
        fields = ["id", "first_name", "last_name", "full_name", "date_of_birth", "date_of_death"]

    def get_full_name(self, obj):
        """
        Формирует полное имя автора.

        Объединяет фамилию и имя автора в строку формата "Фамилия Имя".

        Args:
            obj (Author): Экземпляр модели Author.

        Returns:
            str: Полное имя автора.
        """
        return f"{obj.last_name} {obj.first_name}"


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления жанров книг.

    Преобразует объект Genre в формат, подходящий для передачи через API.
    """

    class Meta:
        """
        Метаданные сериализатора GenreSerializer.

        Определяют модель и поля, подлежащие сериализации.
        """

        model = Genre
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления книг.

    Преобразует объект Book в формат, подходящий для передачи через API.
    Включает подробную информацию об авторе и жанрах книги.

    Attributes:
        author_details (AuthorSerializer): Детальная информация об авторе книги.
        genres (GenreSerializer): Список жанров книги.
    """

    author_details = AuthorSerializer(source="author", read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        """
        Метаданные сериализатора BookSerializer.

        Определяют модель и поля, подлежащие сериализации.
        """

        model = Book
        fields = ["id", "title", "author_details", "genres", "summary", "isbn"]


class BookCheckoutSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления выдачи книг пользователям.

    Преобразует объект BookCheckout в формат, подходящий для передачи через API.
    Включает дополнительную информацию о названии книги и имени пользователя.

    Attributes:
        book_title (ReadOnlyField): Название книги.
        reader_username (ReadOnlyField): Имя пользователя, взявшего книгу.
    """

    book_title = serializers.ReadOnlyField(source="book.title")
    reader_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        """
        Метаданные сериализатора BookCheckoutSerializer.

        Определяют модель и поля, подлежащие сериализации.
        """

        model = BookCheckout
        fields = [
            "id",
            "book",
            "book_title",
            "reader_username",
            "checkout_date",
            "due_date",
            "return_date",
            "is_returned",
        ]
