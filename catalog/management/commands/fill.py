from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создаем категорию, если ее еще нет
        category, created = Category.objects.get_or_create(
            name='Default Category',
            defaults={'description': 'This is a default category description'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new category: {category.name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Using existing category: {category.name}'))

        # Список продуктов для создания
        products = [
            {'name': 'product1', 'category': category},
            {'name': 'product2', 'category': category}
        ]

        # Создаем продукты
        for product in products:
            Product.objects.create(**product)
            self.stdout.write(self.style.SUCCESS(f'Created product: {product["name"]}'))
