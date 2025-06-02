from django.contrib import admin

from catalog.models import Author, Book, BookItem, Wishlist

# Register your models here.
admin.site.register(
    [
        Author,
        Book,
        BookItem,
        Wishlist
    ]
)
