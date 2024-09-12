from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from product.models import Author, Book  # Agora importado de 'product'
from product.factories import AuthorFactory, BookFactory  # Agora importado de 'product.factories'
import faker
from rest_framework_simplejwt.tokens import RefreshToken

class APITests(TestCase):
    def setUp(self):
        # Criação do usuário e geração do token JWT
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Inicialização do Faker
        self.fake = faker.Faker()
        self.fake.seed_instance(0)

    def tearDown(self):
        # Limpeza dos dados após cada teste
        Author.objects.all().delete()
        Book.objects.all().delete()
        User.objects.all().delete()

    def test_create_author(self):
        url = reverse('author-list')
        response = self.client.post(url, {'name': 'Test Author', 'birth_date': '2000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'Test Author')

    def test_create_book(self):
        author = AuthorFactory()
        url = reverse('book-list')
        response = self.client.post(url, {'title': 'Test Book', 'publication_date': '2020-01-01', 'author': author.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_list_authors(self):
        # Limpar antes de criar novos dados para o teste
        Author.objects.all().delete()
        
        AuthorFactory.create_batch(3)
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_books(self):
        # Limpar antes de criar novos dados para o teste
        Book.objects.all().delete()
        
        BookFactory.create_batch(3)
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_author_invalid_data(self):
        url = reverse('author-list')
        response = self.client.post(url, {'name': '', 'birth_date': 'invalid-date'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Author.objects.count(), 0)

    def test_create_book_without_authentication(self):
        self.client.credentials()  # Remove as credenciais
        author = AuthorFactory()
        url = reverse('book-list')
        response = self.client.post(url, {'title': 'Test Book', 'publication_date': '2020-01-01', 'author': author.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_author(self):
        author = AuthorFactory(name='Old Name')
        url = reverse('author-detail', args=[author.id])
        response = self.client.put(url, {'name': 'New Name', 'birth_date': author.birth_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get().name, 'New Name')

    def test_delete_author(self):
        author = AuthorFactory()
        url = reverse('author-detail', args=[author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)
