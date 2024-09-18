
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from books.models import Author
from books.filters import AuthorFilter
from books.serializers import AuthorSerializer

class AuthorList(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter