from django.urls import reverse
from django.test import TestCase, Client
from catalog.models import Book, Author, BookItem, Wishlist
from django.contrib.auth import get_user_model

class BookViewsTestCase(TestCase):
    fixtures = ["catalog/fixtures/test_catalog.json"]

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(username="testuser")
        self.author = Author.objects.get(name="Test Author")
        self.book = Book.objects.get(title="Test Book")

    def test_book_list_view_success(self):
        url = reverse('book_list_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('books', data)
        self.assertEqual(len(data['books']), 1)

        book = data['books'][0]
        expected_keys = {'id', 'title', 'authors', 'isbn', 'publication_year', 'language'}
        self.assertTrue(expected_keys.issubset(book.keys()))

    def test_book_list_view_wrong_method(self):
        url = reverse('book_list_view')
        response = self.client.post(url)
        self.assertIn(response.status_code, [405, 400])

    def test_book_detail_view_success(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.book.id)

    def test_book_detail_view_not_found(self):
        url = reverse('book-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_book_detail_view_wrong_method(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [405, 400])


class BookItemViewsTestCase(TestCase):
    fixtures = ["catalog/fixtures/test_catalog.json"]

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.get(title="Test Book")
        self.book_item = BookItem.objects.get(book=self.book)

    def test_book_item_list_view(self):
        url = reverse('book-item-list', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.json())


class WishlistViewsTestCase(TestCase):
    fixtures = ["catalog/fixtures/test_catalog.json"]

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(username="testuser")
        self.author = Author.objects.get(name="Test Author")
        self.book = Book.objects.get(title="Test Book")
        self.wishlist = Wishlist.objects.get(user=self.user)

    def test_wishlist_list_view_requires_login(self):
        url = reverse('wishlist-list-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_wishlist_list_view_authenticated(self):
        self.client.force_login(self.user)
        url = reverse('wishlist-list-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.json())

    def test_add_to_wishlist(self):
        self.client.force_login(self.user)
        new_book = Book.objects.create(title="Another Book", isbn="9876543210123", publication_year=2021, language="EN")
        new_book.authors.add(self.author)
        url = reverse('add-to-wishlist', args=[new_book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('added', response.json()['message'])

    def test_add_to_wishlist_duplicate(self):
        self.client.force_login(self.user)
        url = reverse('add-to-wishlist', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('already in wishlist', response.json()['message'])

    def test_remove_from_wishlist(self):
        self.client.force_login(self.user)
        url = reverse('remove-from-wishlist', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('removed', response.json()['message'])

    def test_add_to_wishlist_wrong_method(self):
        self.client.force_login(self.user)
        url = reverse('add-to-wishlist', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_remove_from_wishlist_wrong_method(self):
        self.client.force_login(self.user)
        url = reverse('remove-from-wishlist', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
