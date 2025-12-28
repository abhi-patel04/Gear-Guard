"""
Admin configuration for maintenance app.

🔍 EXPLANATION FOR BEGINNERS:
This file customizes how MaintenanceRequest appears in the Django admin panel.
Maintenance requests are the core of the system, so this admin is very detailed.
"""
from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for MaintenanceRequest model.
    """
    
    # List Display - What columns to show
    list_display = [
        'subject',
        'equipment',
        'maintenance_team',
        'request_type',
        'status',
        'assigned_to',
        'scheduled_date',
        'is_overdue_display',
        'created_by',
        'created_at'
    ]
    """
    🔍 EXPLANATION: list_display
    Shows all important request information in a table.
    - 'subject' = What's wrong / what needs to be done
    - 'equipment' = Which equipment needs maintenance
    - 'maintenance_team' = Which team handles it
    - 'request_type' = Corrective or Preventive
    - 'status' = New, In Progress, Repaired, Scrap
    - 'assigned_to' = Which technician is working on it
    - 'scheduled_date' = When preventive maintenance is scheduled
    - 'is_overdue_display' = Custom method showing if overdue
    - 'created_by' = Who created the request
    - 'created_at' = When it was created
    """
    
    # Filters - Sidebar filters
    list_filter = [
        'status',
        'request_type',
        'maintenance_team',
        'equipment__department',  # Filter by equipment's department
        'created_at',
        'scheduled_date'
    ]
    """
    🔍 EXPLANATION: list_filter
    Powerful filtering options in the sidebar.
    - 'status' = Filter by New, In Progress, Repaired, Scrap
    - 'request_type' = Filter by Corrective or Preventive
    - 'maintenance_team' = Filter by team
    - 'equipment__department' = Filter by equipment's department (double underscore = related field)
    - 'created_at' = Filter by creation date
    - 'scheduled_date' = Filter by scheduled date (for preventive)
    
    Example: Click "New" in status filter → Shows only new requests
    Example: Click "IT" in department filter → Shows only IT equipment requests
    """
    
    # Search Fields
    search_fields = [
        'subject',
        'description',
        'equipment__name',  # Search by equipment name
        'equipment__serial_number',  # Search by equipment serial number
        'created_by__username'  # Search by creator's username
    ]
    """
    🔍 EXPLANATION: search_fields
    Search across multiple fields including related fields.
    - 'subject' = Search in request subject
    - 'description' = Search in description
    - 'equipment__name' = Search by equipment name (double underscore = related field)
    - 'equipment__serial_number' = Search by equipment serial number
    - 'created_by__username' = Search by creator's username
    
    Example: Type "Laptop" → Shows all requests for equipment with "Laptop" in name
    """
    
    # Date Hierarchy - Adds date navigation at top
    date_hierarchy = 'created_at'
    """
    🔍 EXPLANATION: date_hierarchy
    Adds a date navigation bar at the top of the list view.
    - Click year → Shows all requests from that year
    - Click month → Shows all requests from that month
    - Click day → Shows all requests from that day
    
    Makes it easy to find requests by date.
    """
    
    # Fieldsets - Group fields in the edit form
    fieldsets = (
        ('Request Information', {
            'fields': ('subject', 'description')
        }),
        ('Equipment & Team', {
            'fields': ('equipment', 'maintenance_team'),
            'description': 'Equipment is required. Maintenance team is usually auto-filled from equipment.'
        }),
        ('Type & Status', {
            'fields': ('request_type', 'status'),
            'description': 'Corrective = Something broke. Preventive = Scheduled maintenance.'
        }),
        ('Assignment', {
            'fields': ('assigned_to',),
            'description': 'Optional: Assign to a specific technician.'
        }),
        ('Scheduling', {
            'fields': ('scheduled_date',),
            'description': 'Required for Preventive maintenance. When should this be performed?'
        }),
        ('Completion', {
            'fields': ('duration_hours', 'completed_at'),
            'description': 'Fill these when request is completed.'
        }),
        ('Creator', {
            'fields': ('created_by',),
            'description': 'User who created this request.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    """
    🔍 EXPLANATION: fieldsets
    Organizes the form into logical sections with descriptions.
    Each section has a description explaining what the fields are for.
    """
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Custom method for list_display
    def is_overdue_display(self, obj):
        """
        🔍 EXPLANATION: Custom method for list_display
        Shows if preventive maintenance is overdue.
        Returns colored text for better visibility.
        """
        if obj.is_overdue():
            return '⚠️ OVERDUE'
        elif obj.request_type == 'Preventive' and obj.scheduled_date:
            return '✓ Scheduled'
        return '-'
    is_overdue_display.short_description = 'Overdue Status'
    is_overdue_display.admin_order_field = 'scheduled_date'
    """
    🔍 EXPLANATION: admin_order_field
    Allows sorting by this custom field.
    Clicking the column header will sort by scheduled_date.
    """
    
    # Actions - Bulk actions
    actions = [
        'mark_as_new',
        'mark_as_in_progress',
        'mark_as_repaired',
        'mark_as_scrap'
    ]
    """
    🔍 EXPLANATION: actions
    Bulk actions to change status of multiple requests at once.
    """
    
    def mark_as_new(self, request, queryset):
        """Mark selected requests as New."""
        count = queryset.update(status='New')
        self.message_user(request, f'{count} requests marked as New.')
    mark_as_new.short_description = 'Mark selected as New'
    
    def mark_as_in_progress(self, request, queryset):
        """Mark selected requests as In Progress."""
        count = queryset.update(status='In Progress')
        self.message_user(request, f'{count} requests marked as In Progress.')
    mark_as_in_progress.short_description = 'Mark selected as In Progress'
    
    def mark_as_repaired(self, request, queryset):
        """Mark selected requests as Repaired."""
        from django.utils import timezone
        count = queryset.update(status='Repaired', completed_at=timezone.now())
        self.message_user(request, f'{count} requests marked as Repaired.')
    mark_as_repaired.short_description = 'Mark selected as Repaired'
    
    def mark_as_scrap(self, request, queryset):
        """
        Mark selected requests as Scrap.
        This will also mark the equipment as scrapped (via signal in Step 10).
        """
        count = queryset.update(status='Scrap')
        self.message_user(request, f'{count} requests marked as Scrap.')
    mark_as_scrap.short_description = 'Mark selected as Scrap'
    
    # Autocomplete for ForeignKey fields (makes selection easier)
    autocomplete_fields = ['equipment', 'maintenance_team', 'assigned_to', 'created_by']
    """
    🔍 EXPLANATION: autocomplete_fields
    Converts ForeignKey dropdowns into searchable autocomplete fields.
    - Instead of scrolling through hundreds of items
    - Type to search and select
    - Much faster for large datasets
    """
    
    # List per page
    list_per_page = 50
    """
    🔍 EXPLANATION: list_per_page
    How many items to show per page in the list view.
    Default is 100, but 50 is more manageable.
    """
