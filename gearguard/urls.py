"""
URL configuration for gearguard project.

🔍 EXPLANATION FOR BEGINNERS:
This file maps URLs (like /equipment/) to views (Python functions that handle requests).
Think of it as a "router" that directs web requests to the right code.

Example:
- User visits: http://localhost:8000/equipment/
- Django looks here and finds: path('equipment/', include('equipment.urls'))
- Django then looks in equipment/urls.py to find the exact view

URL patterns are checked in order (top to bottom).
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import custom admin configuration
from . import admin as gearguard_admin  # This loads the admin site customization

urlpatterns = [
    # Admin panel - Django's built-in database management interface
    # Visit: http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    
    # Include URLs from our apps
    # This means: "When someone visits /accounts/, look in accounts/urls.py"
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('teams/', include('teams.urls', namespace='teams')),
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('maintenance/', include('maintenance.urls', namespace='maintenance')),
    path('', include('dashboard.urls', namespace='dashboard')),  # Root URL goes to dashboard
]

# Serve media files during development
# In production, these should be served by a web server (nginx, Apache)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
