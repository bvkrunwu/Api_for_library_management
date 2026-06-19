from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from library.models import Author, Book, BookCheckout, Genre
from library.permissions import StaffOnlyPermission
from library.serializers import (
    AuthorSerializer,
    BookCheckoutSerializer,
    BookSerializer,
    GenreSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """
    Представление для управления книгами.
    Доступ только для сотрудников библиотеки.
    """

    queryset = Book.objects.prefetch_related("genre").all()
    serializer_class = BookSerializer
    permission_classes = [StaffOnlyPermission]
    filter_backends = [drf_filters.SearchFilter]
    search_fields = [
        "^title",  # Начинающиеся с введённого текста
        "@summary",  # По содержанию аннотации
        "=isbn",  # Точное совпадение ISBN
        "author__first_name",  # По имени автора
        "author__last_name",  # По фамилии автора
        "genre__name",  # По названию жанра
    ]

    @action(detail=False, methods=["get"])
    def advanced_search(self, request):
        """
        Продвинутый поиск книг по дополнительным параметрам.
        """
        queryset = self.get_queryset()
        params = request.query_params

        if "min_year" in params:
            queryset = queryset.filter(author__date_of_birth__year__gte=params["min_year"])

        if "max_year" in params:
            queryset = queryset.filter(author__date_of_birth__year__lte=params["max_year"])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Представление для управления авторами.
    Доступ только для сотрудников библиотеки.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [StaffOnlyPermission]
    filter_backends = [drf_filters.OrderingFilter, drf_filters.SearchFilter]
    search_fields = ["^first_name", "^last_name"]  # Поиск по имени и фамилии
    ordering_fields = ["first_name", "last_name", "date_of_birth"]


class GenreViewSet(viewsets.ModelViewSet):
    """
    Представление для управления жанрами.
    Доступ только для сотрудников библиотеки.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [StaffOnlyPermission]
    filter_backends = [drf_filters.SearchFilter]
    search_fields = ["name"]  # Поиск по названию жанра


class BookCheckoutViewSet(viewsets.ModelViewSet):
    """
    Представление для управления выдачей книг.
    Доступ для всех аутентифицированных пользователей.
    """

    queryset = BookCheckout.objects.select_related("book", "user").all()
    serializer_class = BookCheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["book", "user", "is_returned"]

    def perform_create(self, serializer):
        """
        Автоматически устанавливает текущего пользователя как берущего книгу.
        """
        serializer.save(user=self.request.user)
