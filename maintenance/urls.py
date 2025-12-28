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
    path('api/team/<int:team_id>/members/', views.team_members_api, name='team_members_api'),
    # Work Orders
    path('workorders/', views.workorder_list, name='workorder_list'),
    path('workorders/create/', views.workorder_create, name='workorder_create'),
    path('workorders/<int:pk>/', views.workorder_detail, name='workorder_detail'),
    path('workorders/<int:pk>/edit/', views.workorder_edit, name='workorder_edit'),
    path('workorders/<int:workorder_pk>/activity/create/', views.activity_create, name='activity_create'),
    path('workorders/<int:workorder_pk>/session/create/', views.session_create, name='session_create'),
]

