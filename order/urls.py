from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet, basename='orderitem')  # Isso vai habilitar 'orderitem-list'

urlpatterns = [
    path('', include(router.urls)),
]
