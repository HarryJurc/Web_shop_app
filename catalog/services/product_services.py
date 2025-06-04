from django.conf import settings
from django.core.cache import cache

from catalog.models import Product


def get_products_by_category(category_id):
    cache_key = f'products_category_{category_id}'

    if settings.CACHE_ENABLED:
        products = cache.get(cache_key)
        if products is None:
            products = Product.objects.filter(category_id=category_id, status='published', is_available=True)
            cache.set(cache_key, products, 60 * 15)  # кеш на 15 минут
        return products
    else:
        return Product.objects.filter(category_id=category_id, status='published', is_available=True)
