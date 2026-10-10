"""
URL Configuration for devfolio project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/projects/', include('apps.projects.urls', namespace='projects')),
    path('api/reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('api/showcase/', include('apps.showcase.urls', namespace='showcase')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
