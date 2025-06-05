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
    
class UpdateAmazonIDsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        updates = request.data.get('updates', [])
        updated_books = []
        for update in updates:
            book_id = update.get('id')
            amazon_id = update.get('amazon_id')
            if book_id is not None and amazon_id is not None:
                try:
                    book = Book.objects.get(id=book_id)
                    book.amazon_id = amazon_id
                    book.save()
                    updated_books.append(book_id)
                except Book.DoesNotExist:
                    continue
        return Response({'updated_books': updated_books}, status=status.HTTP_200_OK)