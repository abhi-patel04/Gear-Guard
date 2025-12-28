"""
Admin configuration for equipment app.

🔍 EXPLANATION FOR BEGINNERS:
This file customizes how Equipment appears in the Django admin panel.
"""
from django.contrib import admin
from .models import Equipment, EquipmentCategory


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Equipment model.
    """
    
    # List Display - What columns to show
    list_display = [
        'name',
        'serial_number',
        'department',
        'location',
        'maintenance_team',
        'assigned_employee',
        'is_scrapped',
        'get_active_requests_count',
        'created_at'
    ]
    """
    🔍 EXPLANATION: list_display
    Shows important equipment information in a table format.
    - 'name' = Equipment name
    - 'serial_number' = Unique identifier
    - 'department' = Which department owns it
    - 'location' = Physical location
    - 'maintenance_team' = Which team handles maintenance
    - 'assigned_employee' = Who uses it
    - 'is_scrapped' = Whether it's unusable
    - 'get_active_requests_count' = Number of active requests
    - 'created_at' = When it was added
    """
    
    # Filters - Sidebar filters
    list_filter = [
        'department',
        'maintenance_team',
        'is_scrapped',
        'created_at'
    ]
    """
    🔍 EXPLANATION: list_filter
    Adds filters in the sidebar to quickly find equipment.
    - 'department' = Filter by department (IT, Operations, etc.)
    - 'maintenance_team' = Filter by maintenance team
    - 'is_scrapped' = Show only scrapped or only active equipment
    - 'created_at' = Filter by date added
    
    Example: Click "IT" in department filter → Shows only IT equipment
    """
    
    # Search Fields
    search_fields = [
        'name',
        'serial_number',
        'department',
        'location'
    ]
    """
    🔍 EXPLANATION: search_fields
    Search box searches across multiple fields.
    - 'name' = Search by equipment name
    - 'serial_number' = Search by serial number
    - 'department' = Search by department
    - 'location' = Search by location
    
    Example: Type "Laptop" → Shows all equipment with "Laptop" in name
    Example: Type "IT" → Shows all IT department equipment
    """
    
    # Fieldsets - Group fields in the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'serial_number')
        }),
        ('Location', {
            'fields': ('department', 'location')
        }),
        ('Assignment', {
            'fields': ('maintenance_team', 'assigned_employee'),
            'description': 'Maintenance team handles repairs. Assigned employee is who uses this equipment.'
        }),
        ('Status', {
            'fields': ('is_scrapped',),
            'description': 'If checked, equipment is unusable and cannot have new maintenance requests.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    """
    🔍 EXPLANATION: fieldsets
    Organizes the edit form into logical sections.
    - 'Basic Information' = Name and serial number
    - 'Location' = Department and physical location
    - 'Assignment' = Team and employee
    - 'Status' = Scrapped status
    - 'Timestamps' = Auto-managed dates
    """
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Custom method for list_display
    def get_active_requests_count(self, obj):
        """
        Shows number of active (not completed) maintenance requests.
        """
        return obj.get_active_requests_count()
    get_active_requests_count.short_description = 'Active Requests'
    
    # Actions - Bulk actions on selected items
    actions = ['mark_as_scrapped', 'mark_as_active']
    """
    🔍 EXPLANATION: actions
    Bulk actions allow you to perform operations on multiple items at once.
    - Select multiple equipment in the list
    - Choose an action from dropdown
    - Click "Go"
    """
    
    def mark_as_scrapped(self, request, queryset):
        """
        🔍 EXPLANATION: Custom admin action
        Marks selected equipment as scrapped.
        queryset = Selected equipment items
        """
        count = queryset.update(is_scrapped=True)
        self.message_user(request, f'{count} equipment marked as scrapped.')
    mark_as_scrapped.short_description = 'Mark selected equipment as scrapped'
    
    def mark_as_active(self, request, queryset):
        """
        Marks selected equipment as active (not scrapped).
        """
        count = queryset.update(is_scrapped=False)
        self.message_user(request, f'{count} equipment marked as active.')
    mark_as_active.short_description = 'Mark selected equipment as active'
    
    # Enable autocomplete for this model (used by MaintenanceRequest admin)
    search_fields = ['name', 'serial_number']  # Already defined above, but needed for autocomplete


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for EquipmentCategory model.
    """
    
    # List Display - What columns to show
    list_display = [
        'name',
        'responsible',
        'company',
        'created_at'
    ]
    
    # Filters - Sidebar filters
    list_filter = [
        'company',
        'responsible',
        'created_at'
    ]
    
    # Search Fields
    search_fields = [
        'name',
        'company'
    ]
    
    # Fieldsets - Group fields in the edit form
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'responsible', 'company')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
