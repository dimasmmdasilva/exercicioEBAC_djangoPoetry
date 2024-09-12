from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bem-vindo à página inicial do Bookstore!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bookstore.api.urls')),
    path('product/', include('product.urls')),  # Inclua as URLs do app product
    path('order/', include('order.urls')),  # Inclua as URLs do app order
    path('', home),  # Adiciona a rota raiz
]
