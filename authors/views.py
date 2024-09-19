
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from authors.models import Author
from authors.filters import AuthorFilter
from authors.serializers import AuthorSerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter