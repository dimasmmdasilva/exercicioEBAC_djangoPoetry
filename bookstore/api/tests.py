import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from product.models import Author, Book
from product.factories import AuthorFactory, BookFactory
from order.models import Order, OrderItem
from order.factories import OrderFactory, OrderItemFactory
from decimal import Decimal

class APITests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpassword', is_active=True)

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        Author.objects.all().delete()
        Book.objects.all().delete()

    def tearDown(self):
        super().tearDown()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()

    def test_create_author(self):
        url = reverse('author-list')
        data = {'name': 'Test Author', 'birth_date': '2000-01-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        author = Author.objects.get()
        self.assertEqual(author.name, 'Test Author')

    def test_create_book(self):
        author = AuthorFactory()
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'publication_date': '2020-01-01',
            'author': author.id,
            'price': '29.99',
            'stock': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get()
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.price, Decimal('29.99'))

    def test_create_order(self):
        url = reverse('order-list')
        order_data = {
            'user': self.user.id,
            'total_price': Decimal('150.00')
        }
        response = self.client.post(url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.user, self.user)

    def test_delete_book(self):
        book = BookFactory()
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_order_item(self):
        order = OrderFactory(user=self.user)
        book = BookFactory()
        url = reverse('orderitem-list')
        item_data = {
            'order': order.id,
            'book_id': book.id,
            'quantity': 2,
            'price': Decimal('50.00')
        }
        response = self.client.post(url, item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 1)
        item = OrderItem.objects.get()
        self.assertEqual(item.order.id, order.id)
        self.assertEqual(item.book.id, book.id)
        self.assertEqual(item.quantity, 2)

    def test_update_author(self):
        author = AuthorFactory(name='Old Name', birth_date='1980-01-01')
        url = reverse('author-detail', args=[author.id])
        updated_data = {
            'name': 'New Name',
            'birth_date': '1990-01-01'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.name, 'New Name')
        self.assertEqual(author.birth_date, datetime.date(1990, 1, 1))

    def test_delete_author(self):
        author = AuthorFactory()
        url = reverse('author-detail', args=[author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)
