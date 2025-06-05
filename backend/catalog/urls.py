from django.urls import path
from catalog import views


urlpatterns = [
    path("books/", views.BookListView.as_view(), name="book_list_view"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("books/<int:book_id>/items/", views.BookItemListView.as_view(), name="book-item-list"),
    path("wishlist/", views.WishlistListView.as_view(), name="wishlist-list-view"),
    path("wishlist/add/<int:book_id>/", views.AddToWishlistView.as_view(), name="add-to-wishlist"),
    path("wishlist/remove/<int:book_id>/", views.RemoveFromWishlistView.as_view(), name="remove-from-wishlist"),
    path("books/update-amazon-ids/", views.UpdateAmazonIDsView.as_view(), name="update-amazon-ids"),
]
