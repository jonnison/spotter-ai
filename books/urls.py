from django.urls import path
from rest_framework.routers import SimpleRouter

from books.views import BookViewSet

router = SimpleRouter()
router.register("book", BookViewSet, basename="book")
urlpatterns = router.urls