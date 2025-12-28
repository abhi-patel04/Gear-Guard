"""
URL configuration for maintenance app.

🔍 EXPLANATION:
This file defines URLs for maintenance requests:
- /maintenance/ - List all requests
- /maintenance/create/ - Create new request
- /maintenance/<id>/ - Request detail page
- /maintenance/kanban/ - Kanban board view
- /maintenance/calendar/ - Calendar view
"""
from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.request_list, name='list'),
    path('create/', views.request_create, name='create'),
    path('<int:pk>/', views.request_detail, name='detail'),
    path('<int:pk>/update-status/', views.update_status, name='update_status'),
    path('kanban/', views.kanban_board, name='kanban'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
]

