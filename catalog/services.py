from django.conf import settings
from django.core.cache import cache

from catalog.models import Version


def get_cached_versions_for_product(product):
    if settings.CACHE_ENABLED:  # Если CACHE_ENABLED в настройках проекта
        key = f'product_list_{product.pk}'  # Используем pk продукта для ключа
        version_list = cache.get(key)
        if version_list is None:
            version_list = Version.objects.filter(product=product)  # Используем связь с объектом продукта
            cache.set(key, version_list, timeout=60*15)  # Сохраняем в кэше на 15 минут
    else:
        version_list = Version.objects.filter(product=product)

    return version_list