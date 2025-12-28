"""
Views for maintenance app.

🔍 EXPLANATION:
These views handle maintenance request pages.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import MaintenanceRequest, WorkOrder, Activity, MaintenanceSession
from .forms import MaintenanceRequestForm, StatusUpdateForm, WorkOrderForm, ActivityForm, MaintenanceSessionForm


@login_required
def request_list(request):
    """
    List all maintenance requests.
    
    🔍 EXPLANATION:
    - Shows all requests (filtered by user role)
    - Users see only their requests
    - Technicians see their team's requests
    - Managers see all requests
    - Filtering by status, type, team, equipment
    - Search by subject, description
    """
    # Base queryset - filter by user role
    if request.user.is_staff:  # Managers see all requests
        requests = MaintenanceRequest.objects.all()
    else:
        # Technicians see only their team's requests
        user_teams = request.user.maintenance_teams.all()
        if user_teams.exists():
            requests = MaintenanceRequest.objects.filter(maintenance_team__in=user_teams)
        else:
            # Regular users see only their own requests
            requests = MaintenanceRequest.objects.filter(created_by=request.user)
    
    # Filter: Status
    status = request.GET.get('status')
    if status:
        requests = requests.filter(status=status)
    
    # Filter: Request Type
    request_type = request.GET.get('request_type')
    if request_type:
        requests = requests.filter(request_type=request_type)
    
    # Filter: Equipment
    equipment_id = request.GET.get('equipment')
    if equipment_id:
        requests = requests.filter(equipment_id=equipment_id)
    
    # Filter: Team
    team_id = request.GET.get('team')
    if team_id:
        requests = requests.filter(maintenance_team_id=team_id)
    
    # Search: Subject, Description
    search_query = request.GET.get('search')
    if search_query:
        requests = requests.filter(
            Q(subject__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Order by created date (newest first)
    requests = requests.order_by('-created_at')
    
    # Get filter options
    from teams.models import MaintenanceTeam
    teams = MaintenanceTeam.objects.all().order_by('name')
    from equipment.models import Equipment
    equipment_list = Equipment.objects.filter(is_scrapped=False).order_by('name')
    
    context = {
        'requests': requests,
        'teams': teams,
        'equipment_list': equipment_list,
        'current_status': status,
        'current_request_type': request_type,
        'current_equipment': equipment_id,
        'current_team': team_id,
        'search_query': search_query,
    }
    return render(request, 'maintenance/list.html', context)


@login_required
def request_create(request):
    """
    Create new maintenance request.
    
    🔍 EXPLANATION:
    - Shows form to create request
    - Auto-fills maintenance team from equipment (via JavaScript + view logic)
    - Users can create corrective requests
    - Managers can create preventive requests
    - Sets created_by automatically
    """
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.created_by = request.user
            
            # Auto-assign team from equipment if not set
            if not request_obj.maintenance_team and request_obj.equipment:
                request_obj.maintenance_team = request_obj.equipment.maintenance_team
            
            request_obj.save()
            messages.success(request, f'Maintenance request "{request_obj.subject}" created successfully!')
            return redirect('maintenance:detail', pk=request_obj.pk)
        else:
            # Form is invalid - show error messages
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MaintenanceRequestForm()
        
        # Pre-select equipment if passed in URL
        equipment_id = request.GET.get('equipment')
        if equipment_id:
            try:
                from equipment.models import Equipment
                equipment = Equipment.objects.get(pk=equipment_id)
                form.fields['equipment'].initial = equipment
                # Auto-fill team from equipment
                if equipment.maintenance_team:
                    form.fields['maintenance_team'].initial = equipment.maintenance_team
            except Equipment.DoesNotExist:
                pass
        
        # Pre-fill scheduled_date if passed in URL (from calendar date click)
        scheduled_date = request.GET.get('scheduled_date')
        if scheduled_date:
            try:
                from django.utils.dateparse import parse_datetime
                parsed_date = parse_datetime(scheduled_date)
                if parsed_date:
                    # Format as datetime-local string: YYYY-MM-DDTHH:mm
                    form.fields['scheduled_date'].initial = parsed_date.strftime('%Y-%m-%dT%H:%M')
            except (ValueError, AttributeError):
                pass
        
        # Pre-select request_type if passed in URL (from calendar - should be Preventive)
        request_type = request.GET.get('request_type')
        if request_type in dict(MaintenanceRequest.REQUEST_TYPE_CHOICES):
            form.fields['request_type'].initial = request_type
    
    context = {
        'form': form,
        'title': 'Create Maintenance Request',
        'maintenance_request': None,  # None for create, object for edit
    }
    return render(request, 'maintenance/form.html', context)


@login_required
def request_detail(request, pk):
    """
    Show details of a specific request.
    
    🔍 EXPLANATION:
    - Shows request information
    - Allows status updates (for technicians/managers)
    - Shows equipment details
    - Shows related information
    """
    request_obj = get_object_or_404(MaintenanceRequest, pk=pk)
    
    # Check permissions (technicians can only see their team's requests)
    if not request.user.is_staff:
        user_teams = request.user.maintenance_teams.all()
        if request_obj.maintenance_team not in user_teams and request_obj.created_by != request.user:
            messages.error(request, 'You do not have permission to view this request.')
            return redirect('maintenance:list')
    
    # Status update form
    status_form = None
    if request.method == 'POST' and 'update_status' in request.POST:
        status_form = StatusUpdateForm(request.POST, instance=request_obj)
        if status_form.is_valid():
            updated_request = status_form.save(commit=False)
            
            # Auto-set completed_at when status changes to Repaired
            if updated_request.status == 'Repaired' and request_obj.status != 'Repaired':
                updated_request.completed_at = timezone.now()
            
            updated_request.save()
            messages.success(request, 'Request status updated successfully!')
            return redirect('maintenance:detail', pk=request_obj.pk)
    else:
        status_form = StatusUpdateForm(instance=request_obj)
    
    # Check if user can update status
    can_update_status = (
        request.user.is_staff or  # Managers can update
        (request_obj.maintenance_team and request.user in request_obj.maintenance_team.members.all())  # Team members can update
    )
    
    context = {
        'maintenance_request': request_obj,  # Changed from 'request' to avoid conflict with Django's request object
        'status_form': status_form,
        'can_update_status': can_update_status,
    }
    return render(request, 'maintenance/detail.html', context)


@login_required
def update_status(request, pk):
    """
    Update request status via HTMX (for drag-and-drop).
    
    🔍 EXPLANATION:
    - Called when card is dragged to different column
    - Updates status via POST request
    - Returns updated card HTML
    - Checks permissions before updating
    """
    request_obj = get_object_or_404(MaintenanceRequest, pk=pk)
    
    # Check permissions
    if not request.user.is_staff:
        user_teams = request.user.maintenance_teams.all()
        if request_obj.maintenance_team not in user_teams:
            return render(request, 'maintenance/kanban_card.html', {
                'request': request_obj,
                'error': 'Permission denied'
            }, status=403)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(MaintenanceRequest.STATUS_CHOICES):
            old_status = request_obj.status
            request_obj.status = new_status
            
            # Auto-set completed_at when status changes to Repaired
            if new_status == 'Repaired' and old_status != 'Repaired':
                request_obj.completed_at = timezone.now()
            
            request_obj.save()
    
    # Return updated card HTML
    return render(request, 'maintenance/kanban_card.html', {
        'request': request_obj
    })


@login_required
def kanban_board(request):
    """
    Kanban board view.
    
    🔍 EXPLANATION:
    - Visual workflow board
    - Columns: New, In Progress, Repaired, Scrap
    - Drag-and-drop to change status (will be implemented in Step 8)
    - Filtered by team (for technicians)
    """
    # Base queryset - filter by user role
    if request.user.is_staff:  # Managers see all requests
        requests = MaintenanceRequest.objects.all()
    else:
        # Technicians see only their team's requests
        user_teams = request.user.maintenance_teams.all()
        if user_teams.exists():
            requests = MaintenanceRequest.objects.filter(maintenance_team__in=user_teams)
        else:
            # Regular users see only their own requests
            requests = MaintenanceRequest.objects.filter(created_by=request.user)
    
    # Group by status
    statuses = ['New', 'In Progress', 'Repaired', 'Scrap']
    requests_by_status = {}
    for status in statuses:
        requests_by_status[status] = list(requests.filter(status=status).order_by('-created_at'))
    
    context = {
        'requests_by_status': requests_by_status,
        'statuses': statuses,
    }
    return render(request, 'maintenance/kanban.html', context)


@login_required
def calendar_view(request):
    """
    Calendar view for preventive maintenance.
    
    🔍 EXPLANATION:
    - Shows scheduled preventive maintenance
    - Only shows requests with scheduled_date
    - Managers can schedule new preventive maintenance
    - FullCalendar integration for visual display
    """
    context = {}
    return render(request, 'maintenance/calendar.html', context)


@login_required
def calendar_events(request):
    """
    JSON endpoint for FullCalendar events.
    
    🔍 EXPLANATION:
    - Returns preventive maintenance requests as JSON
    - Format required by FullCalendar
    - Filtered by user role
    """
    from django.http import JsonResponse
    
    # Get preventive maintenance requests with scheduled dates
    requests = MaintenanceRequest.objects.filter(
        request_type='Preventive',
        scheduled_date__isnull=False
    )
    
    # Filter by user role
    if not request.user.is_staff:
        user_teams = request.user.maintenance_teams.all()
        if user_teams.exists():
            requests = requests.filter(maintenance_team__in=user_teams)
        else:
            requests = requests.filter(created_by=request.user)
    
    # Convert to FullCalendar event format
    events = []
    for req in requests:
        # Determine color based on status and overdue
        if req.is_overdue():
            color = '#dc3545'  # Red for overdue
        elif req.status == 'Repaired':
            color = '#198754'  # Green for completed
        elif req.status == 'In Progress':
            color = '#ffc107'  # Yellow for in progress
        else:
            color = '#0dcaf0'  # Cyan for new
        
        events.append({
            'id': req.pk,
            'title': req.subject,
            'start': req.scheduled_date.isoformat(),
            'end': req.scheduled_date.isoformat(),  # Same day event
            'url': f'/maintenance/{req.pk}/',
            'color': color,
            'extendedProps': {
                'equipment': req.equipment.name,
                'team': req.maintenance_team.name if req.maintenance_team else 'Unassigned',
                'status': req.status,
                'assigned_to': (req.assigned_to.get_full_name() or req.assigned_to.username) if req.assigned_to else 'Unassigned',
                'overdue': req.is_overdue(),
            }
        })
    
    return JsonResponse(events, safe=False)


@login_required
def team_members_api(request, team_id):
    """
    JSON endpoint for fetching team members.
    
    🔍 EXPLANATION:
    - Returns list of team members as JSON
    - Used by JavaScript to filter technician dropdown
    - Implements workflow logic: only team members can be assigned
    """
    from django.http import JsonResponse
    from teams.models import MaintenanceTeam
    
    try:
        team = MaintenanceTeam.objects.get(pk=team_id)
        members = team.members.filter(is_active=True).order_by('username')
        
        members_list = []
        for member in members:
            members_list.append({
                'id': member.pk,
                'username': member.username,
                'full_name': member.get_full_name() or member.username,
                'email': member.email or '',
            })
        
        return JsonResponse({
            'success': True,
            'members': members_list
        })
    except MaintenanceTeam.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Team not found'
        }, status=404)


# Work Order Views
@login_required
def workorder_list(request):
    """List all work orders."""
    work_orders = WorkOrder.objects.all().order_by('-date', '-time')
    
    # Filters
    status = request.GET.get('status')
    if status:
        work_orders = work_orders.filter(status=status)
    
    priority = request.GET.get('priority')
    if priority:
        work_orders = work_orders.filter(priority=priority)
    
    assigned_to = request.GET.get('assigned_to')
    if assigned_to:
        work_orders = work_orders.filter(assigned_to_id=assigned_to)
    
    context = {
        'work_orders': work_orders,
        'status_filter': status,
        'priority_filter': priority,
        'assigned_filter': assigned_to,
    }
    return render(request, 'maintenance/workorder_list.html', context)


@login_required
def workorder_create(request):
    """Create new work order."""
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            work_order = form.save()
            messages.success(request, f'Work order {work_order.work_order_number} created successfully!')
            return redirect('maintenance:workorder_detail', pk=work_order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WorkOrderForm()
        # Pre-fill equipment if provided
        equipment_id = request.GET.get('equipment')
        if equipment_id:
            try:
                from equipment.models import Equipment
                equipment = Equipment.objects.get(pk=equipment_id)
                form.fields['equipment'].initial = equipment
            except:
                pass
    
    context = {
        'form': form,
        'title': 'Create Work Order'
    }
    return render(request, 'maintenance/workorder_form.html', context)


@login_required
def workorder_detail(request, pk):
    """View work order details with activities and sessions."""
    from django.db.models import Sum
    work_order = get_object_or_404(WorkOrder, pk=pk)
    activities = work_order.activities.all().order_by('-start_time')
    sessions = work_order.maintenance_sessions.all().order_by('-date', '-start_time')
    
    # Calculate total cost
    total_cost = sessions.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    context = {
        'work_order': work_order,
        'activities': activities,
        'sessions': sessions,
        'total_cost': total_cost,
    }
    return render(request, 'maintenance/workorder_detail.html', context)


@login_required
def workorder_edit(request, pk):
    """Edit work order."""
    work_order = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=work_order)
        if form.is_valid():
            work_order = form.save()
            messages.success(request, f'Work order {work_order.work_order_number} updated successfully!')
            return redirect('maintenance:workorder_detail', pk=work_order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WorkOrderForm(instance=work_order)
    
    context = {
        'form': form,
        'work_order': work_order,
        'title': 'Edit Work Order'
    }
    return render(request, 'maintenance/workorder_form.html', context)


@login_required
def activity_create(request, workorder_pk):
    """Create activity for a work order."""
    work_order = get_object_or_404(WorkOrder, pk=workorder_pk)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.work_order = work_order
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('maintenance:workorder_detail', pk=work_order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm()
    
    context = {
        'form': form,
        'work_order': work_order,
        'title': 'Add Activity'
    }
    return render(request, 'maintenance/activity_form.html', context)


@login_required
def session_create(request, workorder_pk):
    """Create maintenance session for a work order."""
    work_order = get_object_or_404(WorkOrder, pk=workorder_pk)
    
    if request.method == 'POST':
        form = MaintenanceSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.work_order = work_order
            session.save()
            messages.success(request, 'Maintenance session added successfully!')
            return redirect('maintenance:workorder_detail', pk=work_order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MaintenanceSessionForm()
    
    context = {
        'form': form,
        'work_order': work_order,
        'title': 'Add Maintenance Session'
    }
    return render(request, 'maintenance/session_form.html', context)