from django.db import models

from operator import mod
from django.contrib.auth.models import User
from django.db import models
from product.models import Product

# Create your models here.


class OrderStatus(models.TextChoices):
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'


class PaymentStatus(models.TextChoices):
    PAID = 'paid', 'Paid'
    UNPAID = 'un paid', 'Un paid'


class PaymentMode(models.TextChoices):
    COD = 'cod', 'Cash on Delivery'     
    CARD = 'card', 'Card'



class Order(models.Model):
    city = models.CharField(max_length=100 , default='',blank=False)
    zip_code = models.CharField(max_length=20, default='',blank=False)
    street = models.CharField(max_length=100 , default='',blank=False)
    state = models.CharField(max_length=100 , default='',blank=False)
    country = models.CharField(max_length=100 , default='',blank=False)
    phone_no = models.CharField(max_length=20, default='',blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=20, choices=PaymentMode.choices, default=PaymentMode.COD)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
                
                
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100 , default='',blank=False)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.name} in Order {self.order.id}"