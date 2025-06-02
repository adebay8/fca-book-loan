from django.urls import path
from catalog import views


urlpatterns = [
    path("books/", views.book_list_view, name="book_list_view"),
    path("books/<int:book_id>/", views.book_detail_view, name="book-detail"),
    path("books/<int:book_id>/items/", views.book_item_list_view, name="book-item-list"),
    path("wishlist/", views.wishlist_list_view, name="wishlist-list-view"),
    path("wishlist/add/<int:book_id>/", views.add_to_wishlist, name="add-to-wishlist"),
    path("wishlist/remove/<int:book_id>/", views.remove_from_wishlist, name="remove-from-wishlist"),
]
