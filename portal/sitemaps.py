from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product  # Import your Product model

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # This returns all products. You can filter if needed (e.g., active products only)
        return Product.objects.all()

    def location(self, obj):
        # This assumes your Product model has a get_absolute_url method
        # If not, return explicit url like: return f'/product/{obj.id}/'
        return f'/product/{obj.id}/'