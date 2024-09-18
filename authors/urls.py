from django.urls import path
from rest_framework.routers import SimpleRouter

from authors.views import AuthorViewSet

router = SimpleRouter()
router.register("author", AuthorViewSet, basename="author")
urlpatterns = router.urls