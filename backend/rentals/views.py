from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from catalog.models import BookItem
from rentals.models import Rental
from .serializers import ActiveRentalReportSerializer


class BorrowBookItemView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, item_id):
        item = get_object_or_404(BookItem, pk=item_id)
        if not item.is_available:
            return Response(
                {"error": "This item is already borrowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Rental.objects.create(user=request.user, book_item=item)
        item.is_available = False
        item.save(update_fields=["is_available"])
        return Response(
            {
                "message": f"BookItem #{item.id} (“{item.book.title}”) marked as borrowed."
            }
        )


class ReturnBookItemView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, item_id):
        item = get_object_or_404(BookItem, pk=item_id)
        try:
            rental = Rental.objects.get(book_item=item, returned_at__isnull=True)
        except Rental.DoesNotExist:
            return Response(
                {"error": "No active rental found for this item."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rental.returned_at = timezone.now()
        rental.save(update_fields=["returned_at"])
        item.is_available = True
        item.save(update_fields=["is_available"])
        return Response(
            {
                "message": f"BookItem #{item.id} (“{item.book.title}”) returned and marked available. Notifications enqueued."
            }
        )


class ActiveRentalReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        active_rentals = Rental.objects.filter(returned_at__isnull=True).select_related(
            "book_item__book"
        )
        serializer = ActiveRentalReportSerializer(active_rentals, many=True)
        summary = {
            "total_active_rentals": active_rentals.count(),
            "rentals": serializer.data,
        }
        return Response(summary)
