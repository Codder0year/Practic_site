from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='images/users_avatars', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='Страна', **NULLABLE)
    email_token = models.CharField(max_length=270, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

