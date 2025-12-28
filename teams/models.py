"""
Models for teams app.

🔍 EXPLANATION FOR BEGINNERS:
Models = Database tables. Each model class becomes a table in the database.
Each field in the model becomes a column in that table.

Example:
- MaintenanceTeam model → "teams_maintenanceteam" table in database
- name field → "name" column in the table
"""
from django.db import models
from django.contrib.auth.models import User


class MaintenanceTeam(models.Model):
    """
    Maintenance Team Model
    
    🔍 PURPOSE:
    Represents a group of technicians who work together.
    Example: "IT Support Team", "Mechanics Team", "HVAC Team"
    
    🔍 REAL-WORLD EXAMPLE:
    - A factory has 3 teams:
      1. IT Support (handles computers, printers)
      2. Mechanics (handles machines, vehicles)
      3. HVAC (handles air conditioning, heating)
    
    🔍 HOW IT'S USED:
    - Equipment is assigned to a team (e.g., "Laptop #123" → "IT Support Team")
    - Maintenance requests are assigned to teams
    - Technicians see only requests for their team
    - Kanban board filters by team
    - Calendar view groups by team color
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the maintenance team (e.g., 'IT Support', 'Mechanics')"
    )
    """
    🔍 FIELD EXPLANATION: name
    - CharField = Text field with maximum length
    - max_length=100 = Maximum 100 characters
    - unique=True = No two teams can have the same name
    - Example values: "IT Support", "Mechanics", "HVAC Team"
    """
    
    company = models.CharField(
        max_length=200,
        default='My Company',
        help_text="Company name for this team (e.g., 'My Company (San Francisco)')"
    )
    """
    🔍 FIELD EXPLANATION: company
    - CharField = Text field with maximum length
    - max_length=200 = Maximum 200 characters
    - default='My Company' = Default company name
    - Example values: "My Company", "My Company (San Francisco)"
    - Used to display company name for each team member
    """
    
    members = models.ManyToManyField(
        User,
        related_name='maintenance_teams',
        blank=True,
        help_text="Users (technicians) who belong to this team"
    )
    """
    🔍 FIELD EXPLANATION: members
    - ManyToManyField = A user can be in multiple teams, a team can have multiple users
    - User = Django's built-in user model (from django.contrib.auth)
    - related_name='maintenance_teams' = Access a user's teams with: user.maintenance_teams.all()
    - blank=True = Team can exist without members (useful when creating new team)
    
    🔍 RELATIONSHIP EXPLANATION:
    Many-to-Many means:
    - One technician can be in multiple teams (e.g., John is in "IT Support" AND "Weekend On-Call")
    - One team can have multiple technicians (e.g., "IT Support" has John, Jane, Bob)
    
    🔍 HOW IT'S USED:
    - When a technician logs in, we check: user.maintenance_teams.all()
    - We show them only requests assigned to their teams
    - In Kanban board, we filter: requests where team in user.maintenance_teams.all()
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    """
    🔍 FIELD EXPLANATION: created_at
    - DateTimeField = Stores date and time
    - auto_now_add=True = Automatically set when team is created (can't be changed)
    - Example: "2025-12-27 10:30:00"
    - Used for: Tracking when team was created, sorting teams by creation date
    """
    
    updated_at = models.DateTimeField(auto_now=True)
    """
    🔍 FIELD EXPLANATION: updated_at
    - DateTimeField = Stores date and time
    - auto_now=True = Automatically updated every time team is saved
    - Example: "2025-12-27 15:45:00"
    - Used for: Tracking last modification time
    """
    
    class Meta:
        """
        🔍 EXPLANATION: Meta class
        Provides metadata about the model (not stored in database).
        - ordering = Default order when querying teams
        - verbose_name = Human-readable name (for admin panel)
        - verbose_name_plural = Plural form
        """
        ordering = ['name']  # Teams sorted alphabetically by name
        verbose_name = 'Maintenance Team'
        verbose_name_plural = 'Maintenance Teams'
    
    def __str__(self):
        """
        🔍 EXPLANATION: __str__ method
        Returns a string representation of the object.
        Used in:
        - Admin panel (shows "IT Support" instead of "MaintenanceTeam object (1)")
        - Dropdown lists in forms
        - Debugging/printing objects
        """
        return self.name
    
    def get_member_count(self):
        """
        🔍 EXPLANATION: Custom method
        Returns the number of members in this team.
        
        🔍 HOW IT'S USED:
        - Display in team list: "IT Support (5 members)"
        - Dashboard statistics: "Total technicians: 15"
        """
        return self.members.count()
    
    def get_active_requests_count(self):
        """
        🔍 EXPLANATION: Custom method
        Returns the number of active (not completed) requests for this team.
        
        🔍 HOW IT'S USED:
        - Team detail page: "Active Requests: 3"
        - Dashboard widget: "IT Support has 3 open requests"
        """
        # Import here to avoid circular import
        from maintenance.models import MaintenanceRequest
        return MaintenanceRequest.objects.filter(
            maintenance_team=self,
            status__in=['New', 'In Progress']
        ).count()
