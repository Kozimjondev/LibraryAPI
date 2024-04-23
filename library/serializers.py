from rest_framework import serializers

from library.models import Book


class BookSerializer(serializers.ModelSerializer):
    book_type = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(many=False, slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = (
            'title',
            'author',
            'pages',
            'book_type',
            'image',
            'price',
        )


class BookDetailSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    book_type = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    author = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = (
            'owner',
            'title',
            'author',
            'publisher',
            'year',
            'pages',
            'description',
            'book_type',
            'image',
            'file',
            'price',
        )
