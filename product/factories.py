# product/factories.py
import factory
from .models import Author, Book
from faker import Faker
from decimal import Decimal

faker = Faker()

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    
    name = factory.Faker('name')
    birth_date = factory.Faker('date_of_birth', minimum_age=18, maximum_age=75)

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    
    title = factory.Faker('sentence', nb_words=4)
    publication_date = factory.Faker('date_this_decade')
    author = factory.SubFactory(AuthorFactory)
    price = factory.LazyFunction(lambda: Decimal(faker.pydecimal(left_digits=2, right_digits=2, positive=True)))
    stock = factory.Faker('random_int', min=1, max=100)
    