# Generated by Django 5.0.7 on 2024-08-14 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='views_count',
            field=models.PositiveIntegerField(default=0, help_text='Количество просмотров', verbose_name='Просмотров'),
        ),
    ]
