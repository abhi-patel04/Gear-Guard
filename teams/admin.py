"""
Admin configuration for teams app.

🔍 EXPLANATION FOR BEGINNERS:
Django Admin is a built-in web interface for managing your database.
It automatically creates forms to add/edit/delete records.

This file customizes how models appear in the admin panel:
- What columns to show in the list
- What filters to add
- What fields to search
- How to display related objects
"""
from django.contrib import admin
from .models import MaintenanceTeam


@admin.register(MaintenanceTeam)
class MaintenanceTeamAdmin(admin.ModelAdmin):
    """
    Admin configuration for MaintenanceTeam model.
    
    🔍 EXPLANATION:
    @admin.register decorator tells Django to use this class for the MaintenanceTeam model.
    This class customizes how MaintenanceTeam appears in the admin panel.
    """
    
    # List Display - What columns to show in the list view
    list_display = ['name', 'company', 'get_member_count', 'get_active_requests_count', 'created_at']
    """
    🔍 EXPLANATION: list_display
    Defines which columns appear in the admin list view.
    - 'name' = Team name
    - 'get_member_count' = Custom method (shows number of members)
    - 'get_active_requests_count' = Custom method (shows active requests)
    - 'created_at' = When team was created
    
    Example display:
    | Name          | Member Count | Active Requests | Created At      |
    |---------------|--------------|-----------------|-----------------|
    | IT Support    | 5            | 3               | Dec 27, 2025    |
    | Mechanics     | 8            | 2               | Dec 26, 2025    |
    """
    
    # Filters - Sidebar filters for easy filtering
    list_filter = ['created_at']
    """
    🔍 EXPLANATION: list_filter
    Adds filter sidebar on the right side of the list view.
    - 'created_at' = Filter teams by creation date
    
    Users can click filters to show only teams created in a specific time period.
    """
    
    # Search Fields - Search bar at the top
    search_fields = ['name', 'company']
    """
    🔍 EXPLANATION: search_fields
    Adds a search box at the top of the list view.
    - 'name' = Search by team name
    
    Users can type "IT" and it will show all teams with "IT" in the name.
    """
    
    # Fields to show in the detail/edit form
    filter_horizontal = ['members']
    """
    🔍 EXPLANATION: filter_horizontal
    Creates a nice two-column widget for ManyToMany fields.
    - Left column: Available users
    - Right column: Selected team members
    - Users can move users between columns with arrow buttons
    
    This is much better than a dropdown for ManyToMany fields!
    """
    
    # Fieldsets - Group related fields together
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company')
        }),
        ('Team Members', {
            'fields': ('members',),
            'description': 'Select users (technicians) who belong to this team.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Collapsed by default
        }),
    )
    """
    🔍 EXPLANATION: fieldsets
    Groups related fields into sections in the edit form.
    - 'Basic Information' = Team name
    - 'Team Members' = Members selection
    - 'Timestamps' = Created/updated dates (collapsed by default)
    
    Makes the form more organized and easier to use.
    """
    
    # Read-only fields (shown but can't be edited)
    readonly_fields = ['created_at', 'updated_at']
    """
    🔍 EXPLANATION: readonly_fields
    Fields that are displayed but cannot be edited.
    - 'created_at' = Set automatically when created
    - 'updated_at' = Set automatically when saved
    
    These are auto-managed by Django, so users shouldn't edit them manually.
    """
    
    # Custom methods for list_display
    def get_member_count(self, obj):
        """
        🔍 EXPLANATION: Custom method for list_display
        Returns the number of members in the team.
        obj = The MaintenanceTeam instance
        
        Used in list_display to show member count in the list view.
        """
        return obj.get_member_count()
    get_member_count.short_description = 'Members'
    """
    🔍 EXPLANATION: short_description
    Sets the column header name in the list view.
    Without this, column would be named "Get Member Count" (ugly).
    With this, it's named "Members" (clean).
    """
    
    def get_active_requests_count(self, obj):
        """
        🔍 EXPLANATION: Custom method for list_display
        Returns the number of active requests for this team.
        """
        return obj.get_active_requests_count()
    get_active_requests_count.short_description = 'Active Requests'
    
    # Enable autocomplete for this model (used by Equipment and MaintenanceRequest admin)
    # search_fields already defined above, which enables autocomplete
