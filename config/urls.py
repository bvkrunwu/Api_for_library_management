from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API для управления библиотекой",
        default_version="v1",
        description="REST API для управления библиотекой. API предоставляет возможности для управления книгами,"
        "авторами и пользователями, а также для отслеживания выдачи книг пользователям.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ytfrpkkpreim@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("library.urls", namespace="library")),
    path("users/", include("users.urls", namespace="users")),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# Для работы с медиафайлами только для режима разработки (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
