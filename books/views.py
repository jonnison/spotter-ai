
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from books.models import Book
from books.filters import BookFilter
from books.serializers import BookSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter