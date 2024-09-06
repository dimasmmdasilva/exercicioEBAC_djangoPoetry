from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookstore.api"  # O caminho completo para o módulo 'api'
