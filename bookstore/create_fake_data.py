import os
import django
from faker import Faker
import random

print("Configurando as variáveis de ambiente")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from api.models import Author, Book

print("Configurando Faker")
fake = Faker()

print("Criando dados fictícios para autores")
for _ in range(10):
    Author.objects.create(
        name=fake.name(),
        birth_date=fake.date_of_birth(minimum_age=25, maximum_age=90)
    )

print("Criando dados fictícios para livros")
authors = list(Author.objects.all())
for _ in range(50):
    Book.objects.create(
        title=fake.sentence(nb_words=4),
        publication_date=fake.date_this_century(),
        author=random.choice(authors)
    )

print("Dados fictícios criados com sucesso!")
