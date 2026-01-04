from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CardDetails

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # Returns all products that are NOT marked as unavailable
        return CardDetails.objects.exclude(availablity='no')

    def location(self, obj):
        # FIXED: Now matches name='productview' from your urls.py
        return reverse('productview', args=[obj.id])