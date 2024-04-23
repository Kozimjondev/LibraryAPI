from django.shortcuts import render
from rest_framework import viewsets

from library.models import Book
from library.permissions import IsAdminOrReadOnly
from library.serializers import BookSerializer, BookDetailSerializer


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly,]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookSerializer
        return BookDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)