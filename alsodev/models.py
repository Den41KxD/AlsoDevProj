from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token


class Product(models.Model):
    name = models.CharField(max_length=100, default='unknown_prod')
    price = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Product')
    created_at = models.DateTimeField(auto_now=True)


class Picture(models.Model):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    product_to = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Images', default=None)

class TemporaryTokenModel(Token):
    last_active = models.DateTimeField(auto_now=True)