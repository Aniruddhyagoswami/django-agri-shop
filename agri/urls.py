# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),  # This includes the URLs from the portal app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serving media files in development
