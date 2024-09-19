
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from recommendation.models import Favorite
from recommendation.serializers import FavoriteSerializer

class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = []

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    # action recommendations
