"""
Views for equipment app.

🔍 EXPLANATION:
These views handle equipment management pages.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Equipment, EquipmentCategory
from .forms import EquipmentForm, EquipmentCategoryForm


@login_required
def equipment_list(request):
    """
    List all equipment with filtering and search.
    
    🔍 EXPLANATION:
    - Shows all equipment in the system
    - Can be filtered by department, team, scrapped status
    - Can be searched by name, serial number, location
    - Pagination for large lists
    """
    # Get all equipment (exclude scrapped by default)
    equipment_list = Equipment.objects.all()
    
    # Filter: Show scrapped equipment?
    show_scrapped = request.GET.get('show_scrapped', 'false') == 'true'
    if not show_scrapped:
        equipment_list = equipment_list.filter(is_scrapped=False)
    
    # Filter: Department
    department = request.GET.get('department')
    if department:
        equipment_list = equipment_list.filter(department__icontains=department)
    
    # Filter: Maintenance Team
    team_id = request.GET.get('team')
    if team_id:
        equipment_list = equipment_list.filter(maintenance_team_id=team_id)
    
    # Search: Name, Serial Number, Location
    search_query = request.GET.get('search')
    if search_query:
        equipment_list = equipment_list.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Order by name
    equipment_list = equipment_list.order_by('name')
    
    # Get all teams for filter dropdown
    from teams.models import MaintenanceTeam
    teams = MaintenanceTeam.objects.all().order_by('name')
    
    # Get unique departments for filter dropdown
    departments = Equipment.objects.values_list('department', flat=True).distinct().order_by('department')
    
    context = {
        'equipment_list': equipment_list,
        'teams': teams,
        'departments': departments,
        'show_scrapped': show_scrapped,
        'current_department': department,
        'current_team': team_id,
        'search_query': search_query,
    }
    return render(request, 'equipment/list.html', context)


@login_required
def equipment_detail(request, pk):
    """
    Show details of a specific equipment.
    
    🔍 EXPLANATION:
    - Shows equipment information
    - Shows related maintenance requests
    - Has "Create Maintenance Request" button
    - Shows active requests count
    """
    equipment = get_object_or_404(Equipment, pk=pk)
    
    # Get related maintenance requests (most recent first)
    maintenance_requests = equipment.maintenance_requests.all().order_by('-created_at')[:10]
    
    # Get active requests count
    active_requests_count = equipment.get_active_requests_count()
    
    context = {
        'equipment': equipment,
        'maintenance_requests': maintenance_requests,
        'active_requests_count': active_requests_count,
    }
    return render(request, 'equipment/detail.html', context)


@login_required
def equipment_create(request):
    """
    Create new equipment.
    
    🔍 EXPLANATION:
    - Shows form to create new equipment
    - Only staff/managers can create equipment (optional permission check)
    - Saves equipment and redirects to detail page
    """
    # Optional: Check if user has permission
    # if not request.user.is_staff:
    #     messages.error(request, 'You do not have permission to create equipment.')
    #     return redirect('equipment:list')
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f'Equipment "{equipment.name}" created successfully!')
            return redirect('equipment:detail', pk=equipment.pk)
        else:
            # Form has errors - they will be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentForm()
    
    context = {
        'form': form,
        'title': 'Create Equipment',
    }
    return render(request, 'equipment/form.html', context)


@login_required
def equipment_edit(request, pk):
    """
    Edit existing equipment.
    
    🔍 EXPLANATION:
    - Shows form to edit equipment
    - Only staff/managers can edit equipment (optional permission check)
    - Updates equipment and redirects to detail page
    """
    equipment = get_object_or_404(Equipment, pk=pk)
    
    # Optional: Check if user has permission
    # if not request.user.is_staff:
    #     messages.error(request, 'You do not have permission to edit equipment.')
    #     return redirect('equipment:detail', pk=equipment.pk)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f'Equipment "{equipment.name}" updated successfully!')
            return redirect('equipment:detail', pk=equipment.pk)
        else:
            # Form has errors - they will be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentForm(instance=equipment)
    
    context = {
        'form': form,
        'equipment': equipment,
        'title': 'Edit Equipment',
    }
    return render(request, 'equipment/form.html', context)


@login_required
def category_list(request):
    """
    List all equipment categories.
    
    🔍 EXPLANATION:
    - Shows all equipment categories in the system
    - Displays name, responsible person, and company
    """
    categories = EquipmentCategory.objects.all().order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'equipment/category_list.html', context)


@login_required
def category_create(request):
    """
    Create new equipment category.
    
    🔍 EXPLANATION:
    - Shows form to create new category
    - Saves category and redirects to category list
    """
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Equipment category "{category.name}" created successfully!')
            return redirect('equipment:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentCategoryForm()
    
    context = {
        'form': form,
        'title': 'Create Equipment Category',
    }
    return render(request, 'equipment/category_form.html', context)


@login_required
def category_edit(request, pk):
    """
    Edit existing equipment category.
    
    🔍 EXPLANATION:
    - Shows form to edit category
    - Updates category and redirects to category list
    """
    category = get_object_or_404(EquipmentCategory, pk=pk)
    
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Equipment category "{category.name}" updated successfully!')
            return redirect('equipment:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': 'Edit Equipment Category',
    }
    return render(request, 'equipment/category_form.html', context)


@login_required
def category_delete(request, pk):
    """
    Delete equipment category.
    
    🔍 EXPLANATION:
    - Deletes category after confirmation
    - Redirects to category list
    """
    category = get_object_or_404(EquipmentCategory, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Equipment category "{category_name}" deleted successfully!')
        return redirect('equipment:category_list')
    
    context = {
        'category': category,
    }
    return render(request, 'equipment/category_delete.html', context)
