from django.urls import include, path
from rest_framework.routers import DefaultRouter

from library.apps import LibraryConfig
from library.views import AuthorViewSet, BookCheckoutViewSet, BookViewSet, GenreViewSet

app_name = LibraryConfig.name

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"books", BookViewSet, basename="books")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"bookcheckouts", BookCheckoutViewSet, basename="bookcheckouts")

urlpatterns = [path("", include(router.urls))]
