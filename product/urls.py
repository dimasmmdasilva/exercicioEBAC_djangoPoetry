from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.viewsets import BookViewSet, AuthorViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
