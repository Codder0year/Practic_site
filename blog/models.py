from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.CharField(max_length=200, verbose_name='Slug')
    body = models.TextField(verbose_name='Текст')
    preview = models.ImageField(upload_to='images/blog', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    views_count = models.PositiveIntegerField(verbose_name='Просмотров', help_text='Количество просмотров',default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'