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
from .models import Equipment, EquipmentCategory
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
            'category',
            'company',
            'used_for',
            'serial_number',
            'location',
            'maintenance_team',
            'assigned_employee',
            'acquisition_date',
            'description',
            'condition',
            'is_scrapped',
            'has_work_order'
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
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Company (San Francisco)'
            }),
            'used_for': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Office work, Production line'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., SN123456'
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
            'acquisition_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed description of the equipment'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_scrapped': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_work_order': forms.CheckboxInput(attrs={
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
            'name': 'Name',
            'category': 'Equipment Category',
            'company': 'Company',
            'used_for': 'Used For',
            'serial_number': 'Serial Number',
            'location': 'Location',
            'maintenance_team': 'Maintenance Team',
            'assigned_employee': 'Assigned Employee',
            'acquisition_date': 'Acquisition Date',
            'description': 'Description',
            'condition': 'Condition',
            'is_scrapped': 'Is Scrapped?',
            'has_work_order': 'Work Order?'
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
        
        # Filter equipment categories
        self.fields['category'].queryset = EquipmentCategory.objects.all().order_by('name')
        self.fields['category'].empty_label = 'Select a category...'
        
        # Filter maintenance teams (only active teams)
        self.fields['maintenance_team'].queryset = MaintenanceTeam.objects.all().order_by('name')
        self.fields['maintenance_team'].empty_label = 'Select a team...'
        
        # Filter users (only active users)
        from django.contrib.auth.models import User
        self.fields['assigned_employee'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_employee'].empty_label = 'None (unassigned)'
        
        # Make optional fields
        self.fields['serial_number'].required = False
        self.fields['category'].required = False
        self.fields['company'].required = False
        self.fields['used_for'].required = False
        self.fields['acquisition_date'].required = False
        self.fields['description'].required = False
        self.fields['maintenance_team'].required = False
        self.fields['assigned_employee'].required = False
        self.fields['condition'].required = False
        self.fields['is_scrapped'].required = False
        self.fields['has_work_order'].required = False
        
        # Ensure Location is required (it's the only required field besides name)
        self.fields['location'].required = True


class EquipmentCategoryForm(forms.ModelForm):
    """
    Form for creating and editing EquipmentCategory.
    
    🔍 EXPLANATION:
    ModelForm automatically creates form fields from the model.
    """
    
    class Meta:
        model = EquipmentCategory
        fields = [
            'name',
            'responsible',
            'company'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computers, Software, Monitors'
            }),
            'responsible': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Company (San Francisco)'
            }),
        }
        
        labels = {
            'name': 'Category Name',
            'responsible': 'Responsible',
            'company': 'Company'
        }
        
        help_texts = {
            'name': 'Name of the equipment category',
            'responsible': 'User responsible for this category',
            'company': 'Company name for this category'
        }
    
    def __init__(self, *args, **kwargs):
        """
        🔍 EXPLANATION: __init__ method
        Customizes the form when it's created.
        """
        super().__init__(*args, **kwargs)
        
        # Filter users (only active users)
        from django.contrib.auth.models import User
        self.fields['responsible'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['responsible'].empty_label = 'Select a user...'
        
        # Make responsible optional
        self.fields['responsible'].required = False

