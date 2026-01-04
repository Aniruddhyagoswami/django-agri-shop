from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # 1. Add this import


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),  # Includes your portal app URLs
    path(
        "google822615329e5ecb04.html", 
        TemplateView.as_view(template_name="google822615329e5ecb04.html", content_type="text/plain")
    ),
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
