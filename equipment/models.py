"""
Models for equipment app.

🔍 EXPLANATION FOR BEGINNERS:
This file defines the Equipment model, which represents physical assets
that need maintenance (machines, laptops, vehicles, etc.).
"""
from django.db import models
from django.contrib.auth.models import User
from teams.models import MaintenanceTeam


class Equipment(models.Model):
    """
    Equipment Model
    
    🔍 PURPOSE:
    Represents a physical asset that needs maintenance.
    Examples: Laptops, machines, vehicles, printers, HVAC units
    
    🔍 REAL-WORLD EXAMPLE:
    - Company has 50 laptops
    - Each laptop is an Equipment object
    - Laptop #123 breaks → Create MaintenanceRequest for Equipment #123
    - Equipment #123 is assigned to "IT Support Team"
    - When creating request, system auto-fills team from equipment
    
    🔍 HOW IT'S USED:
    - Equipment list page shows all equipment
    - Equipment detail page shows equipment info + related requests
    - When creating maintenance request, user selects equipment
    - System auto-assigns maintenance team from equipment
    - "Scrap" status disables equipment (can't create new requests)
    """
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text="Equipment name (e.g., 'Laptop #123', 'Printer Main Office')"
    )
    """
    🔍 FIELD EXPLANATION: name
    - CharField = Text field
    - max_length=200 = Maximum 200 characters
    - Example: "Laptop #123", "Printer Main Office", "Delivery Van #5"
    - Used in: Equipment list, detail page, dropdown menus
    """
    
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique serial number for identification"
    )
    """
    🔍 FIELD EXPLANATION: serial_number
    - CharField = Text field
    - unique=True = No two equipment can have the same serial number
    - blank=True, null=True = Optional field (some equipment might not have serial numbers)
    - Example: "SN123456789", "ABC-2024-001"
    - Used for: Tracking, warranty claims, inventory management
    """
    
    # Location Information
    department = models.CharField(
        max_length=100,
        help_text="Department that owns this equipment (e.g., 'IT', 'Operations', 'Sales')"
    )
    """
    🔍 FIELD EXPLANATION: department
    - CharField = Text field
    - Example: "IT", "Operations", "Sales", "HR"
    - Used for: Filtering equipment by department, reports
    """
    
    location = models.CharField(
        max_length=200,
        help_text="Physical location (e.g., 'Building A, Floor 2, Room 205')"
    )
    """
    🔍 FIELD EXPLANATION: location
    - CharField = Text field
    - Example: "Building A, Floor 2, Room 205", "Warehouse", "Main Office"
    - Used for: Finding equipment, technician navigation, reports
    """
    
    # Relationships
    maintenance_team = models.ForeignKey(
        MaintenanceTeam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment',
        help_text="Team responsible for maintaining this equipment"
    )
    """
    🔍 FIELD EXPLANATION: maintenance_team
    - ForeignKey = Links to another model (MaintenanceTeam)
    - on_delete=models.SET_NULL = If team is deleted, set this field to NULL (don't delete equipment)
    - null=True, blank=True = Optional (equipment might not be assigned to a team yet)
    - related_name='equipment' = Access team's equipment with: team.equipment.all()
    
    🔍 RELATIONSHIP EXPLANATION:
    ForeignKey means:
    - One equipment belongs to ONE team (e.g., "Laptop #123" → "IT Support Team")
    - One team can have MANY equipment (e.g., "IT Support Team" has 50 laptops)
    
    🔍 HOW IT'S USED (AUTOMATION):
    - When user creates maintenance request and selects equipment
    - System automatically fills: request.maintenance_team = equipment.maintenance_team
    - This is the "auto-assign team" feature!
    """
    
    assigned_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_equipment',
        help_text="Employee currently using this equipment (optional)"
    )
    """
    🔍 FIELD EXPLANATION: assigned_employee
    - ForeignKey = Links to User model
    - on_delete=models.SET_NULL = If user is deleted, set to NULL (don't delete equipment)
    - null=True, blank=True = Optional (equipment might not be assigned to anyone)
    - related_name='assigned_equipment' = Access user's equipment with: user.assigned_equipment.all()
    
    🔍 HOW IT'S USED:
    - Track who uses which equipment
    - "My Equipment" page: user.assigned_equipment.all()
    - When equipment breaks, notify assigned employee
    """
    
    # Status
    is_scrapped = models.BooleanField(
        default=False,
        help_text="If True, equipment is unusable and cannot have new maintenance requests"
    )
    """
    🔍 FIELD EXPLANATION: is_scrapped
    - BooleanField = True or False
    - default=False = New equipment is not scrapped
    - Used for: Disabling equipment, preventing new requests
    
    🔍 HOW IT'S USED (AUTOMATION):
    - When maintenance request status = "Scrap"
    - System automatically sets: equipment.is_scrapped = True
    - Scrapped equipment is hidden from equipment list (or shown with warning)
    - Cannot create new requests for scrapped equipment
    """
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    """
    🔍 FIELD EXPLANATION: created_at
    - DateTimeField = Stores date and time
    - auto_now_add=True = Set when equipment is created
    - Used for: Tracking when equipment was added to system
    """
    
    updated_at = models.DateTimeField(auto_now=True)
    """
    🔍 FIELD EXPLANATION: updated_at
    - DateTimeField = Stores date and time
    - auto_now=True = Updated every time equipment is saved
    - Used for: Tracking last modification
    """
    
    class Meta:
        """
        🔍 EXPLANATION: Meta class
        Provides metadata about the model.
        """
        ordering = ['-created_at']  # Newest equipment first
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
    
    def __str__(self):
        """
        🔍 EXPLANATION: __str__ method
        Returns string representation for admin panel and forms.
        """
        return f"{self.name} ({self.department})"
    
    def get_active_requests_count(self):
        """
        🔍 EXPLANATION: Custom method
        Returns count of active (not completed) maintenance requests.
        
        🔍 HOW IT'S USED:
        - Equipment detail page: "Active Requests: 2"
        - Equipment list: Show badge with request count
        """
        # This will work after we create MaintenanceRequest model
        return self.maintenance_requests.filter(
            status__in=['New', 'In Progress']
        ).count() if hasattr(self, 'maintenance_requests') else 0
    
    def can_create_request(self):
        """
        🔍 EXPLANATION: Custom method
        Checks if new maintenance requests can be created for this equipment.
        
        🔍 HOW IT'S USED:
        - In equipment detail page: Show/hide "Create Request" button
        - In request form: Validate that equipment is not scrapped
        """
        return not self.is_scrapped
