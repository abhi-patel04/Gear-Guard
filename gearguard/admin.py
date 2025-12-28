"""
Custom admin site configuration.

🔍 EXPLANATION FOR BEGINNERS:
This file customizes the Django admin site appearance.
It changes the header, title, and other admin site settings.
"""
from django.contrib import admin

# Customize admin site header and title
admin.site.site_header = "GearGuard Administration"
admin.site.site_title = "GearGuard Admin"
admin.site.index_title = "Welcome to GearGuard Maintenance Tracker"
"""
🔍 EXPLANATION:
- site_header = Text shown at the top of every admin page
- site_title = Text shown in browser tab title
- index_title = Text shown on the admin homepage

This makes the admin panel clearly branded as "GearGuard" instead of "Django Administration".
"""

