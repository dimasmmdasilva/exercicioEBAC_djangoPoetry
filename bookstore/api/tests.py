from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from product.models import Author, Book  # Certifique-se que os modelos estão corretos
from product.factories import AuthorFactory, BookFactory  # Certifique-se que as factories estão na pasta certa
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

    # Teste de criação de autor
    def test_create_author(self):
        url = reverse('author-list')
        response = self.client.post(url, {
            'name': 'Test Author', 
            'birth_date': '2000-01-01'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        author = Author.objects.get()
        self.assertEqual(author.name, 'Test Author')  # Verificar se o nome foi corretamente atribuído
        self.assertEqual(str(author), 'Test Author')  # Testando a função __str__

    # Teste de criação de livro
    def test_create_book(self):
        author = AuthorFactory()
        url = reverse('book-list')
        response = self.client.post(url, {
            'title': 'Test Book', 
            'publication_date': '2020-01-01', 
            'author': author.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get()
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, author)  # Verificar se o autor foi associado corretamente

    # Teste de listagem de autores
    def test_list_authors(self):
        Author.objects.all().delete()  # Limpar antes de criar novos dados
        
        AuthorFactory.create_batch(3)
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        for author in response.data:
            self.assertIn('name', author)  # Garantir que os autores possuem o campo "name"

    # Teste de listagem de livros
    def test_list_books(self):
        Book.objects.all().delete()  # Limpar antes de criar novos dados
        
        BookFactory.create_batch(3)
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        for book in response.data:
            self.assertIn('title', book)  # Garantir que os livros possuem o campo "title"

    # Teste de criação de autor com dados inválidos
    def test_create_author_invalid_data(self):
        url = reverse('author-list')
        response = self.client.post(url, {
            'name': '', 
            'birth_date': 'invalid-date'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Author.objects.count(), 0)

    # Teste de criação de livro sem autenticação
    def test_create_book_without_authentication(self):
        self.client.credentials()  # Remove as credenciais para simular a falta de autenticação
        author = AuthorFactory()
        url = reverse('book-list')
        response = self.client.post(url, {
            'title': 'Test Book', 
            'publication_date': '2020-01-01', 
            'author': author.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de atualização de autor
    def test_update_author(self):
        author = AuthorFactory(name='Old Name')
        url = reverse('author-detail', args=[author.id])
        response = self.client.put(url, {
            'name': 'New Name', 
            'birth_date': author.birth_date
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get().name, 'New Name')

    # Teste de deleção de autor
    def test_delete_author(self):
        author = AuthorFactory()
        url = reverse('author-detail', args=[author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)
