import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token


def user_directory_path(instance, filename):
    dir_name = str(instance.product_to.id)
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(dir_name, filename)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Product')
    created_at = models.DateTimeField(auto_now=True)


class Picture(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    product_to = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Images', default=None)


class TemporaryTokenModel(Token):
    last_active = models.DateTimeField(auto_now=True)
