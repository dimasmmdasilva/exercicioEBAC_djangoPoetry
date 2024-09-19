# order/factories.py
import factory
from django.contrib.auth.models import User
from product.factories import BookFactory
from .models import Order, OrderItem

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    book = factory.SubFactory(BookFactory)
    quantity = factory.Faker('pyint', min_value=1, max_value=5)
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)

    @factory.post_generation
    def validate_ids(self, create, extracted, **kwargs):
        assert self.order.id is not None, "Order ID is None"
        assert self.book.id is not None, "Book ID is None"
