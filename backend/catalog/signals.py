from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from catalog.models import Wishlist

@receiver(post_save, sender=User)
def create_user_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)

# catalog/signals.py
from .models import BookItem, Wishlist

@receiver(post_save, sender=BookItem)
def notify_wishlisters_on_availability(sender, instance, created, **kwargs):
    if instance.is_available:
        book = instance.book
        
        available_count = BookItem.objects.filter(book=book, is_available=True).count()
        if available_count == 1:
            wishes = Wishlist.objects.filter(books__id=book.id)
            for wish in wishes:
                # Check if already notified (optional, if NotificationLog is used)
                # if not NotificationLog.objects.filter(user=wish.user, book=book, type='availability').exists():
                print(f"Notifying {wish.user.username} about availability of {book.title}")
                # Optionally log notification
                # NotificationLog.objects.create(user=wish.user, book=book, type='availability')
