import factory
from .models import Author, Book

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')
    birth_date = factory.Faker('date_of_birth')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentece', nb_words=4)
    publication_date = factory.Faker('date')
    author = factory.Faker(AuthorFactory)