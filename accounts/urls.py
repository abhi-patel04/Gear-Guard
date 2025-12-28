"""
URL configuration for accounts app.

🔍 EXPLANATION:
This file defines URLs for user authentication:
- /accounts/login/ - Login page
- /accounts/logout/ - Logout
- /accounts/register/ - User registration
"""
from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Login/Logout URLs (using Django's built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    # Profile and settings pages
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    # Password change (for logged-in users)
    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url=reverse_lazy('accounts:password_change_done')
    ), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
]

