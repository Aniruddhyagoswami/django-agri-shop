from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # 1. Add this import
from django.contrib.sitemaps.views import sitemap # 1. Import this
from portal.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),  # Includes your portal app URLs
    path(
        "google822615329e5ecb04.html", 
        TemplateView.as_view(template_name="google822615329e5ecb04.html", content_type="text/plain")
    ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
