"""
Models for maintenance app.

🔍 EXPLANATION FOR BEGINNERS:
This file defines the MaintenanceRequest model, which represents
a maintenance job (either corrective or preventive).
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from equipment.models import Equipment
from teams.models import MaintenanceTeam


class MaintenanceRequest(models.Model):
    """
    Maintenance Request Model
    
    🔍 PURPOSE:
    Represents a maintenance job that needs to be performed.
    Can be either:
    - Corrective: Something broke, needs fixing (reactive)
    - Preventive: Scheduled maintenance to prevent problems (proactive)
    
    🔍 REAL-WORLD EXAMPLE:
    CORRECTIVE:
    - User: "My laptop won't turn on!"
    - Creates request → Equipment: "Laptop #123"
    - System auto-assigns team: "IT Support"
    - Technician fixes it → Status: "Repaired"
    
    PREVENTIVE:
    - Manager: "Schedule monthly printer maintenance"
    - Creates request → Equipment: "Printer Main Office"
    - Sets scheduled_date: "2025-01-15"
    - Appears on calendar
    - Technician performs on scheduled date
    
    🔍 HOW IT'S USED:
    - Request creation form (users create requests)
    - Kanban board (visual workflow: New → In Progress → Repaired)
    - Calendar view (preventive maintenance scheduling)
    - Dashboard statistics (open requests, overdue requests)
    - Request detail page (view/update request)
    """
    
    # Status Choices
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Repaired', 'Repaired'),
        ('Scrap', 'Scrap'),
    ]
    """
    🔍 EXPLANATION: STATUS_CHOICES
    Defines valid values for the status field.
    - 'New' = Request just created, not started
    - 'In Progress' = Technician is working on it
    - 'Repaired' = Completed successfully
    - 'Scrap' = Equipment is beyond repair, mark as scrapped
    
    🔍 HOW IT'S USED:
    - Kanban board columns: One column per status
    - Filtering: Show only "New" requests
    - Statistics: Count requests by status
    """
    
    # Request Type Choices
    REQUEST_TYPE_CHOICES = [
        ('Corrective', 'Corrective'),
        ('Preventive', 'Preventive'),
    ]
    """
    🔍 EXPLANATION: REQUEST_TYPE_CHOICES
    Defines the type of maintenance request.
    - 'Corrective' = Something broke, needs fixing (reactive)
    - 'Preventive' = Scheduled maintenance to prevent problems (proactive)
    
    🔍 HOW IT'S USED:
    - Corrective: No scheduled_date needed, fix ASAP
    - Preventive: Must have scheduled_date, appears on calendar
    - Reports: Separate statistics for corrective vs preventive
    """
    
    # Basic Information
    subject = models.CharField(
        max_length=200,
        help_text="Brief description of the issue or maintenance task"
    )
    """
    🔍 FIELD EXPLANATION: subject
    - CharField = Text field
    - max_length=200 = Maximum 200 characters
    - Example: "Laptop won't turn on", "Monthly printer maintenance"
    - Used in: Request list, detail page, notifications
    """
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the issue or maintenance task"
    )
    """
    🔍 FIELD EXPLANATION: description
    - TextField = Long text field (unlimited length)
    - blank=True = Optional field
    - Example: "Laptop was working yesterday, today it won't boot. Tried charging, no response."
    - Used in: Request detail page, technician reference
    """
    
    # Relationships
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
        help_text="Equipment that needs maintenance"
    )
    """
    🔍 FIELD EXPLANATION: equipment
    - ForeignKey = Links to Equipment model
    - on_delete=models.CASCADE = If equipment is deleted, delete all its requests
    - related_name='maintenance_requests' = Access equipment's requests: equipment.maintenance_requests.all()
    
    🔍 RELATIONSHIP EXPLANATION:
    - One equipment can have MANY requests (e.g., "Laptop #123" has 5 requests over time)
    - One request belongs to ONE equipment
    
    🔍 HOW IT'S USED:
    - Equipment detail page: Show all requests for this equipment
    - Request form: User selects equipment from dropdown
    - Auto-assign team: request.maintenance_team = equipment.maintenance_team
    """
    
    maintenance_team = models.ForeignKey(
        MaintenanceTeam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_requests',
        help_text="Team responsible for this request (auto-filled from equipment)"
    )
    """
    🔍 FIELD EXPLANATION: maintenance_team
    - ForeignKey = Links to MaintenanceTeam model
    - on_delete=models.SET_NULL = If team is deleted, set to NULL (don't delete request)
    - null=True, blank=True = Optional (but usually auto-filled)
    - related_name='maintenance_requests' = Access team's requests: team.maintenance_requests.all()
    
    🔍 RELATIONSHIP EXPLANATION:
    - One team can have MANY requests
    - One request belongs to ONE team
    
    🔍 HOW IT'S USED (AUTOMATION):
    - When user selects equipment in request form
    - JavaScript/Django automatically fills: maintenance_team = equipment.maintenance_team
    - Technicians see only requests for their team
    - Kanban board filters by team
    """
    
    # Request Type and Status
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default='Corrective',
        help_text="Type of maintenance: Corrective (breakdown) or Preventive (scheduled)"
    )
    """
    🔍 FIELD EXPLANATION: request_type
    - CharField = Text field
    - choices=REQUEST_TYPE_CHOICES = Only allows 'Corrective' or 'Preventive'
    - default='Corrective' = Most requests are corrective (something broke)
    
    🔍 HOW IT'S USED:
    - Corrective: No scheduled_date required, fix ASAP
    - Preventive: Must have scheduled_date, appears on calendar
    - Form validation: If Preventive, require scheduled_date
    - Calendar view: Only shows Preventive requests
    """
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='New',
        help_text="Current status of the request"
    )
    """
    🔍 FIELD EXPLANATION: status
    - CharField = Text field
    - choices=STATUS_CHOICES = Only allows: New, In Progress, Repaired, Scrap
    - default='New' = New requests start as "New"
    
    🔍 HOW IT'S USED:
    - Kanban board: Columns match status values
    - Workflow: New → In Progress → Repaired
    - Filtering: Show only "New" requests
    - Statistics: Count by status
    - Automation: If status = "Scrap", set equipment.is_scrapped = True
    """
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests',
        help_text="Technician assigned to this request (optional)"
    )
    """
    🔍 FIELD EXPLANATION: assigned_to
    - ForeignKey = Links to User model
    - on_delete=models.SET_NULL = If user is deleted, set to NULL
    - null=True, blank=True = Optional (request can exist without assignment)
    - related_name='assigned_requests' = Access user's assignments: user.assigned_requests.all()
    
    🔍 HOW IT'S USED:
    - Technician dashboard: Show my assigned requests
    - Request detail: Show who's working on it
    - Notifications: Notify assigned technician
    - Kanban board: Show assigned technician on card
    """
    
    # Scheduling (for Preventive Maintenance)
    scheduled_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Scheduled date/time for preventive maintenance (only for Preventive type)"
    )
    """
    🔍 FIELD EXPLANATION: scheduled_date
    - DateTimeField = Stores date and time
    - null=True, blank=True = Optional (only needed for Preventive)
    - Example: "2025-01-15 10:00:00"
    
    🔍 HOW IT'S USED:
    - Calendar view: Shows preventive maintenance on scheduled date
    - Overdue detection: If scheduled_date < today and status != "Repaired" → Overdue
    - Dashboard: Show overdue requests
    - Form validation: If request_type = "Preventive", require scheduled_date
    """
    
    # Completion Information
    duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Time taken to complete the maintenance (in hours)"
    )
    """
    🔍 FIELD EXPLANATION: duration_hours
    - DecimalField = Stores decimal numbers
    - max_digits=5, decimal_places=2 = Maximum 999.99 hours
    - null=True, blank=True = Optional (filled when completed)
    - Example: 2.5 (2 hours 30 minutes)
    
    🔍 HOW IT'S USED:
    - Reports: Average time per request
    - Statistics: Total maintenance hours
    - Technician performance: Time taken per technician
    """
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date/time when request was completed"
    )
    """
    🔍 FIELD EXPLANATION: completed_at
    - DateTimeField = Stores date and time
    - null=True, blank=True = Set when status changes to "Repaired"
    - Used for: Reports, statistics, completion tracking
    """
    
    # Creator Information
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_requests',
        help_text="User who created this request"
    )
    """
    🔍 FIELD EXPLANATION: created_by
    - ForeignKey = Links to User model
    - on_delete=models.SET_NULL = If user is deleted, set to NULL (keep request)
    - related_name='created_requests' = Access user's created requests: user.created_requests.all()
    
    🔍 HOW IT'S USED:
    - Request detail: Show who created it
    - User dashboard: "My Requests" = user.created_requests.all()
    - Notifications: Notify creator when status changes
    """
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    """
    🔍 FIELD EXPLANATION: created_at
    - DateTimeField = Stores date and time
    - auto_now_add=True = Set when request is created
    - Used for: Sorting, filtering, reports
    """
    
    updated_at = models.DateTimeField(auto_now=True)
    """
    🔍 FIELD EXPLANATION: updated_at
    - DateTimeField = Stores date and time
    - auto_now=True = Updated every time request is saved
    - Used for: Tracking last modification
    """
    
    class Meta:
        """
        🔍 EXPLANATION: Meta class
        Provides metadata about the model.
        """
        ordering = ['-created_at']  # Newest requests first
        verbose_name = 'Maintenance Request'
        verbose_name_plural = 'Maintenance Requests'
    
    def __str__(self):
        """
        🔍 EXPLANATION: __str__ method
        Returns string representation for admin panel and forms.
        """
        return f"{self.subject} - {self.get_status_display()}"
    
    def is_overdue(self):
        """
        🔍 EXPLANATION: Custom method
        Checks if preventive maintenance is overdue.
        
        🔍 HOW IT'S USED:
        - Dashboard: Show overdue requests
        - Calendar: Highlight overdue items
        - Notifications: Alert managers about overdue maintenance
        
        🔍 LOGIC:
        - Only applies to Preventive requests
        - Overdue if: scheduled_date < today AND status != "Repaired"
        """
        if self.request_type != 'Preventive' or not self.scheduled_date:
            return False
        if self.status == 'Repaired':
            return False
        return self.scheduled_date < timezone.now()
    
    def mark_completed(self):
        """
        🔍 EXPLANATION: Custom method
        Marks request as completed and sets completion timestamp.
        
        🔍 HOW IT'S USED:
        - When technician updates status to "Repaired"
        - Automatically sets completed_at = now
        """
        self.status = 'Repaired'
        self.completed_at = timezone.now()
        self.save()
    
    def get_duration_display(self):
        """
        🔍 EXPLANATION: Custom method
        Returns formatted duration string.
        
        🔍 HOW IT'S USED:
        - Request detail page: "Duration: 2.5 hours"
        - Reports: Display duration in readable format
        """
        if self.duration_hours:
            return f"{self.duration_hours} hours"
        return "Not set"
