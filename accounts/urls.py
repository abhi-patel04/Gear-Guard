"""
URL configuration for accounts app.

🔍 EXPLANATION:
This file defines URLs for user authentication:
- /accounts/login/ - Login page
- /accounts/logout/ - Logout
- /accounts/register/ - User registration
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Login/Logout URLs (using Django's built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]

