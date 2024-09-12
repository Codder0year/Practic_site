from django.test import TestCase
from django.urls import reverse

from catalog.models import Product, Category
from users.models import User


# Create your tests here.
class TestCatalog(TestCase):

    def test_contacts_page(self):
        # Запрашиваем страницу контактов
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)  # проверяем что страница верна
        self.assertContains(response, 'Контакты')

    def test_catalog_page(self):
        # Запрашиваем страницу каталога
        response = self.client.get(reverse('catalog:home'))  # Замените на ваш правильный URL
        self.assertEqual(response.status_code, 200)  # проверяем что страница верна


class ProductDetailViewTest(TestCase):

    def create_user(self):
        # Создаем пользователя
        user = User.objects.create(
            email='testuser2@test.com',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('testpass')
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user()
        self.user.is_active = True
        self.user.save()  # Сохраняем изменения

        self.category = Category.objects.create(
            name='Test2 Category',
            description='Для тестирования',
        )

        # Создаем продукт для тестирования
        self.product = Product.objects.create(
            name='Test2 Product',
            description='Для тестирования',
            price=29.99,
            category=self.category,
            image='path/to/image.jpg',
            is_available=True,
            is_updated=False,
            owner=self.user,
            is_published=True
        )

    def test_product_detail_page(self):
        # URL для просмотра продукта
        url = reverse('catalog:product_detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Проверяем, что страница отображается

    def test_edit_product(self):
        # URL для редактирования продукта
        edit_url = reverse('catalog:update_product', kwargs={'pk': self.product.pk})
        response = self.client.get(edit_url)
        # Редактирование продукта
        response = self.client.post(edit_url, {
            'name': "Test2 Product",
            'description': 'Редактирование продукта',
            'price': '39.99',  # Используем Decimal для цены
            'category': self.category.pk,
            'image': 'path/to/updated_image.jpg',
            'is_available': True,
            'is_updated': True,
            'owner': self.user.pk,
            'is_published': True
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что страница редиректится
        self.product.refresh_from_db()  # Проверка, что продукт был изменен
        self.assertEqual(self.product.name, "Test2 Product")
        self.assertEqual(self.product.description, 'Редактирование продукта')
        self.assertEqual(self.product.price, '39.99')  # Используем Decimal для цены
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.image, 'path/to/updated_image.jpg')
        self.assertEqual(self.product.is_available, True)
        self.assertEqual(self.product.is_updated, True)
        self.assertEqual(self.product.owner, self.user)
        self.assertEqual(self.product.is_published, True)

    def test_delete_product(self):
        # URL для удаления продукта
        delete_url = reverse('catalog:delete_product', kwargs={'pk': self.product.pk})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница отображается
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)  # Проверяем, что страница редиректится
        # Проверка, что продукт был удален
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())