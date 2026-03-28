from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.TextChoices):
    Computers = 'computers'
    Food = 'food'
    Kids = 'kids'
    Home = 'home'
    Phone = 'phone'


class Product(models.Model):
    
    name = models.CharField(max_length=255, default="", blank=False )
    description = models.TextField(max_length=255, default="", blank=False)
    price = models.DecimalField(max_digits=100, decimal_places=2,default=0)
    brand = models.CharField(max_length=255, default="", blank=False)
    category = models.CharField(max_length=40,choices=Category.choices)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name
    
    
    
class Review(models.Model):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=255, default="", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment
    