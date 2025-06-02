from django.db import models

from core.models import BaseTimeStampedModel

class Author(BaseTimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Book(BaseTimeStampedModel):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    publication_year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=20)
    amazon_id = models.CharField(max_length=20, blank=True, null=True)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

class BookItem(BaseTimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='items')
    condition = models.CharField(max_length=50, default='Good')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book.title} - Item #{self.id}"
    
class Wishlist(BaseTimeStampedModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='wishlist')
    books = models.ManyToManyField(Book, related_name='wishlists', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"