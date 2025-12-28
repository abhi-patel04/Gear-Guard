"""
Views for accounts app.

🔍 EXPLANATION:
Views are Python functions that handle web requests.
When a user visits a URL, Django calls the corresponding view function.
The view processes the request and returns a response (usually HTML).
"""
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


@login_required
def profile_view(request):
    """Simple profile page for the logged-in user."""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def settings_view(request):
    """
    Settings page: allows editing basic profile fields (first name, last name, email)
    and provides a link to change password.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:settings')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/settings.html', {'form': form})

def register(request):
    """
    User registration view.
    
    🔍 EXPLANATION:
    - If user submits form (POST), create new user account
    - If user just visits page (GET), show registration form
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    """
    Custom logout view.
    
    🔍 EXPLANATION:
    - Logs out the user
    - Redirects to login page
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
