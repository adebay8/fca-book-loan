from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from catalog.models import Book, Wishlist
from .serializers import BookSerializer, BookItemSerializer, WishlistBookSerializer

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Book.objects.all().prefetch_related('authors')
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(authors__name__icontains=author)
        return queryset.distinct()

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all().prefetch_related('authors')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookItemListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        items = book.items.all()
        serializer = BookItemSerializer(items, many=True)
        return Response({'book_id': book_id, 'items': serializer.data})

class WishlistListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist = request.user.wishlist.books.all()
        serializer = WishlistBookSerializer(wishlist, many=True)
        return Response({'books': serializer.data})

class AddToWishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        if wishlist.books.filter(id=book.id).exists():
            return Response({'message': f"Book '{book.title}' is already in wishlist"}, status=status.HTTP_200_OK)
        wishlist.books.add(book)
        return Response({'message': f"Book '{book.title}' added to wishlist"})

class RemoveFromWishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        wishlist = request.user.wishlist
        wishlist.books.remove(book)
        return Response({'message': f"Book '{book.title}' removed from wishlist"})