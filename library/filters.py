from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ('book_type', 'pages')