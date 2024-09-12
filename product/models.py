from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Relacionamento com Author
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço do Livro
    stock = models.PositiveIntegerField()  # Quantidade em estoque

    def __str__(self):
        return self.title
