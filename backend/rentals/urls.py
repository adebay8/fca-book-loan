from django.urls import path
from rentals.views import BorrowBookItemView, ReturnBookItemView, ActiveRentalReportView

urlpatterns = [
    path("borrow/<int:item_id>/", BorrowBookItemView.as_view(), name="borrow-bookitem"),
    path("return/<int:item_id>/", ReturnBookItemView.as_view(), name="return-bookitem"),
    path("report/active-rentals/", ActiveRentalReportView.as_view(), name="active-rental-report"),
]
