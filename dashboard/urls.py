"""
URL configuration for dashboard app.

🔍 EXPLANATION:
This file defines URLs for the dashboard:
- / - Homepage/dashboard (root URL)
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
]

