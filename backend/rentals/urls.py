from django.urls import path

from rentals import views


urlpatterns = [
    path("borrow/<int:item_id>/", views.borrow_book_item, name="borrow-bookitem"),
    path("return/<int:item_id>/", views.return_book_item, name="return-bookitem"),
    path("report/active-rentals/", views.active_rental_report, name="active-rental-report"),
]
