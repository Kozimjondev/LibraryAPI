from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from library.filters import BookFilter
from library.models import Book
from library.permissions import IsAdminOrReadOnly
from library.serializers import BookSerializer, BookDetailSerializer


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = BookFilter
    search_fields = ['title', 'author', ]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookSerializer
        return BookDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
