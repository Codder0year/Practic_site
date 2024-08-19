from django.db import models

from users.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products', null=True, blank=True)
    is_available = models.BooleanField(default=True, null=True, blank=True)
    is_updated = models.BooleanField(default=False, null=True, blank=True)
    owner = models.ForeignKey(User,verbose_name='владелец', help_text='Владелец товара', blank=True, null=True, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
            ('can_edit_any_product', 'Может редактировать любой продукт'),
            ('can_change_category', 'Может менять категорию любого продукта'),
        ]


class Contacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    message = models.TextField()


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product model
    number_version = models.IntegerField()
    name_version = models.CharField(max_length=100)
    current_version = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Product.name} - {self.name_version}'

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
