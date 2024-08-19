# Generated by Django 5.0.7 on 2024-08-14 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.CharField(max_length=200, verbose_name='Slug')),
                ('body', models.TextField(verbose_name='Текст')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Превью')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('views_count', models.IntegerField(default=0, verbose_name='Просмотров')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
