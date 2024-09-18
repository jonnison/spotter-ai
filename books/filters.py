from django_filters import rest_framework as filters
from django.db.models import Q

from books.models import Book


class BookFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    search = filters.CharFilter(method='filter_search',name='search')
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(authors__author__name__icontains=value)
        )

    class Meta:
        model = Book
        fields = ['name', 'query']
