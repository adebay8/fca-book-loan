from rest_framework import serializers
from rentals.models import Rental

class ActiveRentalReportSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book_item.book.title")
    book_item_id = serializers.IntegerField(source="book_item.id")
    rented_by = serializers.CharField(source="user.username")
    rented_at = serializers.SerializerMethodField()
    days_rented = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = [
            "book_title",
            "book_item_id",
            "rented_by",
            "rented_at",
            "days_rented",
        ]

    def get_rented_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    def get_days_rented(self, obj):
        from django.utils import timezone
        return (timezone.now() - obj.created_at).days
