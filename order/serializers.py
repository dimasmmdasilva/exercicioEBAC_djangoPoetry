from rest_framework import serializers
from product.models import Book
from .models import Order, OrderItem
from product.serializers import BookSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
        source='book'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'book_id', 'quantity', 'price']

    def create(self, validated_data):
        # Extraia 'book_id' diretamente dos validated_data utilizando o 'source' definido
        book = validated_data.pop('book', None)
        # Agora crie o OrderItem com o livro correto
        order_item = OrderItem.objects.create(book=book, **validated_data)
        return order_item

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'items']
