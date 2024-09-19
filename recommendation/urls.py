from django.urls import path
from rest_framework.routers import SimpleRouter

from recommendation.views import FavoriteViewSet

router = SimpleRouter()
router.register("favorite", FavoriteViewSet, basename="favorite")
urlpatterns = router.urls