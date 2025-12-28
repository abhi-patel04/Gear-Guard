"""
Django settings for gearguard project.

🔍 EXPLANATION FOR BEGINNERS:
This file configures your Django project. Think of it as the "control center" that tells Django:
- Which apps to use (like equipment, maintenance, teams)
- Where to find templates (HTML files)
- Where to find static files (CSS, JavaScript, images)
- Database settings
- Security settings

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = the root folder of your project (Geare-Guard/)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
# This key encrypts session data. Never share it publicly!
SECRET_KEY = 'django-insecure-djpm$*6-qshtfq7%pfr8wmdn&49&i20=gvg+eo%&2fo03bb%=o'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True shows detailed error pages (helpful for development)
DEBUG = True

ALLOWED_HOSTS = []  # In production, add your domain here


# Application definition
# INSTALLED_APPS = List of all Django apps your project uses
# Think of apps as "modules" - each handles a specific feature
INSTALLED_APPS = [
    # Django's built-in apps (come with Django)
    'django.contrib.admin',          # Admin panel (database management UI)
    'django.contrib.auth',           # User authentication (login/logout)
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # Session management
    'django.contrib.messages',       # Flash messages (success/error notifications)
    'django.contrib.staticfiles',    # Static file handling (CSS, JS, images)
    
    # Third-party apps
    'django_htmx',                   # HTMX for dynamic UI updates without full page reloads
    
    # Our custom apps (the features we're building)
    'accounts',                      # User accounts and authentication
    'teams',                         # Maintenance teams (groups of technicians)
    'equipment',                     # Equipment/assets management
    'maintenance',                   # Maintenance requests and workflows
    'dashboard',                     # Dashboard with statistics and overview
]

# MIDDLEWARE = Code that runs on every request (like security checks, authentication)
# They process requests in order (top to bottom) and responses in reverse
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling
    'django.middleware.common.CommonMiddleware',          # Common operations
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF protection (security)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking protection
    'django_htmx.middleware.HtmxMiddleware',             # HTMX support (for dynamic UI)
]

ROOT_URLCONF = 'gearguard.urls'

# TEMPLATES = Configuration for HTML templates
# Templates are HTML files that Django fills with data
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Look for templates in the 'templates' folder
        'APP_DIRS': True,  # Also look in each app's 'templates' folder
        'OPTIONS': {
            'context_processors': [
                # These make certain variables available in ALL templates
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Makes 'request' available
                'django.contrib.auth.context_processors.auth',  # Makes 'user' available
                'django.contrib.messages.context_processors.messages',  # Makes messages available
            ],
        },
    },
]

WSGI_APPLICATION = 'gearguard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Static files = files that don't change (CSS, JS, images)
# In production, these are served by a web server, not Django
STATIC_URL = 'static/'  # URL prefix for static files (e.g., /static/css/style.css)
STATICFILES_DIRS = [BASE_DIR / 'static']  # Where to find static files during development
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Where to collect static files for production

# Media files (user-uploaded files)
# Media files = files uploaded by users (e.g., equipment photos)
MEDIA_URL = 'media/'  # URL prefix for media files
MEDIA_ROOT = BASE_DIR / 'media'  # Where to store uploaded files

# Default primary key field type
# Every Django model needs a primary key (unique ID)
# BigAutoField = auto-incrementing integer (1, 2, 3, ...)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout URLs
# When Django needs to redirect to login, use this URL
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:index'  # Where to go after successful login
LOGOUT_REDIRECT_URL = 'accounts:login'  # Where to go after logout
