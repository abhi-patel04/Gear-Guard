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
    # Equipment Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]

