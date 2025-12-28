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
