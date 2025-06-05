from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from catalog.models import Book, Wishlist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def book_list_view(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request method, only GET allowed")
    title = request.GET.get("title")
    author = request.GET.get("author")
    queryset = Book.objects.all().prefetch_related("authors")

    if title:
        queryset = queryset.filter(title__icontains=title)
    if author:
        queryset = queryset.filter(authors__name__icontains=author)

    queryset = queryset.distinct()

    books = []
    for book in queryset:
        books.append({
            "id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "language": book.language,
            "publication_year": book.publication_year,
            "authors": [author.name for author in book.authors.all()],
            "available_copies": book.items.filter(is_available=True).count(),
        })

    return JsonResponse({
        "books": books,
    })

def book_detail_view(request, book_id):
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request method, only GET allowed")
    book = get_object_or_404(Book.objects.prefetch_related("authors"), pk=book_id)
    data = {
        "id": book.id,
        "title": book.title,
        "isbn": book.isbn,
        "language": book.language,
        "publication_year": book.publication_year,
        "authors": [author.name for author in book.authors.all()],
        "total_copies": book.items.count(),
        "available_copies": book.items.filter(is_available=True).count(),
    }
    return JsonResponse(data)

def book_item_list_view(request, book_id):
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request method, only GET allowed")
    book = get_object_or_404(Book, pk=book_id)
    items = book.items.all()
    item_data = [
        {
            "id": item.id,
            "condition": item.condition,
            "is_available": item.is_available,
        }
        for item in items
    ]
    return JsonResponse({"book_id": book_id, "items": item_data})

@login_required
def wishlist_list_view(request):
    wishlist = request.user.wishlist.books.all()
    data = [
        {
            "id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "authors": [author.name for author in book.authors.all()]
        }
        for book in wishlist
    ]
    return JsonResponse({"books": data})

@login_required
def add_to_wishlist(request, book_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method, only POST allowed")
    
    book = get_object_or_404(Book, id=book_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if wishlist.books.filter(id=book.id).exists():
        return JsonResponse({"message": f"Book '{book.title}' is already in wishlist"}, status=200)
    wishlist.books.add(book)
    return JsonResponse({"message": f"Book '{book.title}' added to wishlist"})


@login_required
def remove_from_wishlist(request, book_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method, only POST allowed")

    book = get_object_or_404(Book, id=book_id)
    wishlist = request.user.wishlist
    wishlist.books.remove(book)
    return JsonResponse({"message": f"Book '{book.title}' removed from wishlist"})


"""
,
  {
    "model": "catalog.Wishlist",
    "pk": 1,
    "fields": {
      "user": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "books": [1]
    }
  }
"""