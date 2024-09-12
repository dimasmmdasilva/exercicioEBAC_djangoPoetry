# api/factories.py
import factory
import faker

faker.Faker.seed(0)  # Semente para reprodutibilidade

from .models import Author, Book

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    
    name = factory.Faker('name')
    birth_date = factory.Faker('date_of_birth')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    
    title = factory.Faker('sentence', nb_words=4)
    publication_date = factory.Faker('date')
    author = factory.SubFactory(AuthorFactory)
