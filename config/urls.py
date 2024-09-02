from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),  # Подключаем URL-ы приложения 'catalog'
    path('blog/', include('blog.urls', namespace='blog')),  # Подключаем URL-ы приложения 'blog'
    path('users/', include('users.urls', namespace='users')),  # Подключаем URL-ы приложения 'users'
    path('mailsender/', include('mailsender.urls', namespace='mailsender')),  # Подключаем URL-ы приложения'mailsender'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
