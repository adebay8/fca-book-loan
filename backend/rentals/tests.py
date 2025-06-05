from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Book, BookItem, Author
from rentals.models import Rental


class RentalTests(TestCase):
    fixtures = ["test_catalog.json", "test_rentals.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=2)
        self.book_item = BookItem.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_borrow_book_item(self):
        self.book_item.is_available = True
        self.book_item.save()
        url = reverse("borrow-bookitem", args=[self.book_item.id])
        response = self.client.post(url)
        self.book_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.book_item.is_available)
        self.assertTrue(Rental.objects.filter(book_item=self.book_item, returned_at__isnull=True).exists())

    def test_return_book_item(self):
        self.book_item.is_available = False
        self.book_item.save()
        url = reverse("return-bookitem", args=[self.book_item.id])
        response = self.client.post(url)
        self.book_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.book_item.is_available)
        rental = Rental.objects.get(book_item=self.book_item)
        self.assertIsNotNone(rental.returned_at)

    def test_active_rental_report(self):
        url = reverse("active-rental-report")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_active_rentals", data)
        self.assertIn("rentals", data)
        self.assertGreaterEqual(data["total_active_rentals"], 0)
