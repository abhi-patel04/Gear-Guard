"""
URL configuration for equipment app.

🔍 EXPLANATION:
This file defines URLs for equipment management:
- /equipment/ - List all equipment
- /equipment/<id>/ - Equipment detail page
- /equipment/create/ - Create new equipment
- /equipment/<id>/edit/ - Edit equipment
"""
from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.equipment_list, name='list'),
    path('create/', views.equipment_create, name='create'),
    path('<int:pk>/', views.equipment_detail, name='detail'),
    path('<int:pk>/edit/', views.equipment_edit, name='edit'),
]

