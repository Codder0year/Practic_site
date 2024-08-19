from django.contrib import admin

from catalog.models import Category, Product, Version


# Register your models here.
# @admin.register
# class CategoryAdmin(admin.ModelAdmin):

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('name_version', 'number_version')
