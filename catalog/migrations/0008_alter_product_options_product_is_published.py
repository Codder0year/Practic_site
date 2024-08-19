# Generated by Django 5.0.7 on 2024-08-19 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_product_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_unpublish_product', 'Может отменять публикацию продукта'), ('can_edit_any_product', 'Может редактировать любой продукт'), ('can_change_category', 'Может менять категорию любого продукта')], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
