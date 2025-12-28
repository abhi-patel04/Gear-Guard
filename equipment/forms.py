"""
Forms for equipment app.

🔍 EXPLANATION FOR BEGINNERS:
Forms are HTML forms with validation logic.
Django forms handle:
- HTML generation
- Data validation
- Error messages
- CSRF protection
"""
from django import forms
from .models import Equipment
from teams.models import MaintenanceTeam


class EquipmentForm(forms.ModelForm):
    """
    Form for creating and editing Equipment.
    
    🔍 EXPLANATION:
    ModelForm automatically creates form fields from the model.
    - Each model field becomes a form field
    - Validation rules come from the model
    - Saves data directly to the model
    """
    
    class Meta:
        model = Equipment
        fields = [
            'name',
            'serial_number',
            'department',
            'location',
            'maintenance_team',
            'assigned_employee',
            'is_scrapped'
        ]
        """
        🔍 EXPLANATION: fields
        Specifies which model fields to include in the form.
        Order matters - fields appear in this order in the form.
        """
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Laptop #123'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., SN123456'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., IT, Operations, Sales'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Building A, Room 205'
            }),
            'maintenance_team': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_employee': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_scrapped': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        """
        🔍 EXPLANATION: widgets
        Customizes how form fields are rendered in HTML.
        - TextInput = Single-line text input
        - Select = Dropdown menu
        - CheckboxInput = Checkbox
        - attrs = HTML attributes (class, placeholder, etc.)
        """
        
        labels = {
            'name': 'Equipment Name',
            'serial_number': 'Serial Number',
            'department': 'Department',
            'location': 'Location',
            'maintenance_team': 'Maintenance Team',
            'assigned_employee': 'Assigned Employee',
            'is_scrapped': 'Mark as Scrapped'
        }
        """
        🔍 EXPLANATION: labels
        Custom labels for form fields.
        Without this, labels would be "name", "serial_number" (ugly).
        With this, labels are "Equipment Name", "Serial Number" (nice).
        """
        
        help_texts = {
            'serial_number': 'Optional: Unique serial number for identification',
            'maintenance_team': 'Team responsible for maintaining this equipment',
            'assigned_employee': 'Optional: Employee currently using this equipment',
            'is_scrapped': 'If checked, equipment is unusable and cannot have new maintenance requests'
        }
        """
        🔍 EXPLANATION: help_texts
        Helpful text shown below form fields.
        Guides users on what to enter.
        """
    
    def __init__(self, *args, **kwargs):
        """
        🔍 EXPLANATION: __init__ method
        Customizes the form when it's created.
        - Sets queryset for ForeignKey fields (filters options)
        - Adds custom attributes
        """
        super().__init__(*args, **kwargs)
        
        # Filter maintenance teams (only active teams)
        self.fields['maintenance_team'].queryset = MaintenanceTeam.objects.all().order_by('name')
        self.fields['maintenance_team'].empty_label = 'Select a team...'
        
        # Filter users (only active users)
        from django.contrib.auth.models import User
        self.fields['assigned_employee'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_employee'].empty_label = 'None (unassigned)'
        
        # Make serial_number optional
        self.fields['serial_number'].required = False
        self.fields['maintenance_team'].required = False
        self.fields['assigned_employee'].required = False

