from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# 1. Add these imports
from django.contrib.sitemaps.views import sitemap
from portal.sitemaps import ProductSitemap

# 2. Define the sitemap dictionary
sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),

    # Google Verification (Keep this)
    path(
        "google822615329e5ecb04.html", 
        TemplateView.as_view(template_name="google822615329e5ecb04.html", content_type="text/plain")
    ),

    # 3. Add the Sitemap URL here
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)