"""
Views for dashboard app.

🔍 EXPLANATION:
These views handle the main dashboard/homepage.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from equipment.models import Equipment
from maintenance.models import MaintenanceRequest
from teams.models import MaintenanceTeam


@login_required
def index(request):
    """
    Dashboard homepage.
    
    🔍 EXPLANATION:
    - Shows statistics (total equipment, open requests, etc.)
    - Shows recent activity
    - Different widgets based on user role
    - Status breakdown charts
    - Recent requests feed
    
    🔍 HOW IT WORKS:
    - Queries the database for equipment and requests
    - Filters based on user role (technicians see only their team's requests)
    - Calculates statistics
    - Gets recent activity
    - Passes data to template
    """
    # Base queryset for requests - filter by user role
    if request.user.is_staff:  # Managers see all requests
        requests_queryset = MaintenanceRequest.objects.all()
        equipment_queryset = Equipment.objects.all()
    else:
        # Technicians see only their team's requests
        user_teams = request.user.maintenance_teams.all()
        if user_teams.exists():
            requests_queryset = MaintenanceRequest.objects.filter(maintenance_team__in=user_teams)
            equipment_queryset = Equipment.objects.filter(maintenance_team__in=user_teams)
        else:
            # Regular users see only their own requests
            requests_queryset = MaintenanceRequest.objects.filter(created_by=request.user)
            equipment_queryset = Equipment.objects.filter(assigned_employee=request.user)
    
    # Equipment Statistics
    total_equipment = equipment_queryset.filter(is_scrapped=False).count()
    scrapped_equipment = equipment_queryset.filter(is_scrapped=True).count()
    
    # Request Statistics
    total_requests = requests_queryset.count()
    open_requests = requests_queryset.filter(status__in=['New', 'In Progress']).count()
    
    # Overdue Requests
    overdue_requests = requests_queryset.filter(
        request_type='Preventive',
        status__in=['New', 'In Progress']
    )
    overdue_count = sum(1 for req in overdue_requests if req.is_overdue())
    
    # Completed Today
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    completed_today = requests_queryset.filter(
        status='Repaired',
        completed_at__gte=today_start
    ).count()
    
    # Status Breakdown
    status_breakdown = requests_queryset.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Request Type Breakdown
    type_breakdown = requests_queryset.values('request_type').annotate(
        count=Count('id')
    ).order_by('request_type')
    
    # Recent Requests (last 10)
    recent_requests = requests_queryset.order_by('-created_at')[:10]
    
    # Recent Completed (last 5)
    recent_completed = requests_queryset.filter(
        status='Repaired'
    ).order_by('-completed_at')[:5]
    
    # My Requests (for regular users)
    my_requests = None
    if not request.user.is_staff and not request.user.maintenance_teams.exists():
        my_requests = requests_queryset.filter(created_by=request.user).count()
    
    # Team Statistics (for managers)
    team_stats = None
    if request.user.is_staff:
        team_stats = MaintenanceTeam.objects.annotate(
            request_count=Count('maintenance_requests'),
            active_request_count=Count('maintenance_requests', filter=Q(maintenance_requests__status__in=['New', 'In Progress']))
        ).order_by('-active_request_count')[:5]
    
    # Equipment by Department
    equipment_by_department = equipment_queryset.filter(
        is_scrapped=False
    ).values('department').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    context = {
        # Statistics
        'total_equipment': total_equipment,
        'scrapped_equipment': scrapped_equipment,
        'total_requests': total_requests,
        'open_requests': open_requests,
        'overdue_requests': overdue_count,
        'completed_today': completed_today,
        'my_requests': my_requests,
        
        # Breakdowns
        'status_breakdown': status_breakdown,
        'type_breakdown': type_breakdown,
        
        # Recent Activity
        'recent_requests': recent_requests,
        'recent_completed': recent_completed,
        
        # Team Stats (managers only)
        'team_stats': team_stats,
        
        # Equipment Stats
        'equipment_by_department': equipment_by_department,
        
        # User Info
        'is_manager': request.user.is_staff,
        'is_technician': request.user.maintenance_teams.exists(),
    }
    return render(request, 'dashboard/index.html', context)
