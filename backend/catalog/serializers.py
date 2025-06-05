from rest_framework import serializers
from catalog.models import Book

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    available_copies = serializers.SerializerMethodField()
    total_copies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'language', 'publication_year',
            'authors', 'available_copies', 'total_copies'
        ]

    def get_authors(self, obj):
        return [author.name for author in obj.authors.all()]

    def get_available_copies(self, obj):
        return obj.items.filter(is_available=True).count()

    def get_total_copies(self, obj):
        return obj.items.count()

class BookItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    condition = serializers.CharField()
    is_available = serializers.BooleanField()

class WishlistBookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'authors']

    def get_authors(self, obj):
        return [author.name for author in obj.authors.all()]
