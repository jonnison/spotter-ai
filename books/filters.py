from django_filters import rest_framework as filters
from django.db.models import Q

from books.models import Book
from authors.models import Author


class BookFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains',field_name="name")
    search = filters.CharFilter(method='filter_search')
    
    def filter_search(self, queryset, name, value):
        authors = Author.objects.filter(name__icontains=value)
        return queryset.filter(
            Q(name__icontains=value)
            | Q(authors__in=authors)
        )

    class Meta:
        model = Book
        fields = ['name', 'search']
