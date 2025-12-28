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
        ('Rejected', 'Rejected'),
        ('Scrap', 'Scrap'),
    ]
    """
    🔍 EXPLANATION: STATUS_CHOICES
    Defines valid values for the status field.
    - 'New' = Request just created, not started
    - 'In Progress' = Technician is working on it
    - 'Repaired' = Completed successfully
    - 'Rejected' = Request was rejected by admin/manager
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
    
    # Priority field from wireframe
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium',
        help_text="Priority level of the maintenance request"
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
    
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Due date for completing this maintenance request"
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


class WorkOrder(models.Model):
    """
    Work Order Model
    
    🔍 PURPOSE:
    Represents a work order for maintenance tasks.
    Work orders can be created from maintenance requests and assigned to employees.
    """
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    work_order_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique work order number"
    )
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='work_orders',
        help_text="Equipment this work order is for"
    )
    
    maintenance_request = models.ForeignKey(
        'MaintenanceRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='work_orders',
        help_text="Related maintenance request (optional)"
    )
    
    date = models.DateField(
        help_text="Date of the work order"
    )
    
    time = models.TimeField(
        help_text="Time of the work order"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open',
        help_text="Current status of the work order"
    )
    
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium',
        help_text="Priority level"
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_work_orders',
        help_text="Employee assigned to this work order"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description of the work to be done"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
    
    def __str__(self):
        return f"WO-{self.work_order_number} - {self.equipment.name}"
    
    def save(self, *args, **kwargs):
        if not self.work_order_number:
            # Auto-generate work order number
            from django.db.models import Max
            last_wo = WorkOrder.objects.aggregate(Max('id'))
            if last_wo['id__max']:
                try:
                    last_obj = WorkOrder.objects.get(id=last_wo['id__max'])
                    last_num = int(last_obj.work_order_number.split('-')[-1])
                    self.work_order_number = f"WO-{last_num + 1:04d}"
                except:
                    self.work_order_number = f"WO-{WorkOrder.objects.count() + 1:04d}"
            else:
                self.work_order_number = "WO-0001"
        super().save(*args, **kwargs)


class Activity(models.Model):
    """
    Activity Model
    
    🔍 PURPOSE:
    Represents an activity performed during maintenance work.
    Activities track what work was done, time spent, costs, and parts used.
    """
    
    ACTIVITY_TYPE_CHOICES = [
        ('Inspection', 'Inspection'),
        ('Repair', 'Repair'),
        ('Replacement', 'Replacement'),
        ('Cleaning', 'Cleaning'),
        ('Calibration', 'Calibration'),
        ('Testing', 'Testing'),
        ('Other', 'Other'),
    ]
    
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text="Work order this activity belongs to"
    )
    
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPE_CHOICES,
        help_text="Type of activity performed"
    )
    
    description = models.TextField(
        help_text="Description of the activity"
    )
    
    start_time = models.DateTimeField(
        help_text="Start time of the activity"
    )
    
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="End time of the activity"
    )
    
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Cost of this activity"
    )
    
    parts_used = models.TextField(
        blank=True,
        help_text="Parts or materials used"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.work_order.work_order_number}"
    
    def get_duration(self):
        """Calculate duration in hours"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 3600
        return None


class MaintenanceSession(models.Model):
    """
    Maintenance Session Model
    
    🔍 PURPOSE:
    Tracks time spent, cost per hour, and total cost for maintenance work.
    Used for timesheet and cost tracking.
    """
    
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='maintenance_sessions',
        help_text="Work order this session belongs to"
    )
    
    date = models.DateField(
        help_text="Date of the maintenance session"
    )
    
    start_time = models.TimeField(
        help_text="Start time"
    )
    
    end_time = models.TimeField(
        null=True,
        blank=True,
        help_text="End time"
    )
    
    cost_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Cost per hour for this session"
    )
    
    duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Duration in hours (hrs:mins format)"
    )
    
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Total cost for this session"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = 'Maintenance Session'
        verbose_name_plural = 'Maintenance Sessions'
    
    def __str__(self):
        return f"Session - {self.work_order.work_order_number} - {self.date}"
    
    def calculate_total_cost(self):
        """Calculate total cost based on duration and cost per hour"""
        if self.duration_hours and self.cost_per_hour:
            self.total_cost = self.duration_hours * self.cost_per_hour
        return self.total_cost
    
    def save(self, *args, **kwargs):
        self.calculate_total_cost()
        super().save(*args, **kwargs)
