# api/tests.py
from contextvars import Token
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book
from .factories import AuthorFactory, BookFactory
import faker

class APITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.fake = faker.Faker()
        self.fake.seed_instance(0)

    def test_create_author(self):
        response = self.client.post('/api/authors/', {'name': 'Test Author', 'birth_date': '2000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'Test Author')

    def test_create_book(self):
        author = AuthorFactory()
        response = self.client.post('/api/books/', {'title': 'Test Book', 'publication_date': '2020-01-01', 'author': author.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_list_authors(self):
        AuthorFactory.create_batch(3)
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_books(self):
        BookFactory.create_batch(3)
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)