"""
Forms for maintenance app.

🔍 EXPLANATION FOR BEGINNERS:
Forms for creating and updating maintenance requests.
"""
from django import forms
from .models import MaintenanceRequest
from equipment.models import Equipment
from teams.models import MaintenanceTeam


class MaintenanceRequestForm(forms.ModelForm):
    """
    Form for creating and editing Maintenance Requests.
    
    🔍 EXPLANATION:
    - Auto-fills maintenance team from equipment (via JavaScript)
    - Validates that preventive requests have scheduled_date
    - Sets created_by automatically
    """
    
    class Meta:
        model = MaintenanceRequest
        fields = [
            'subject',
            'description',
            'equipment',
            'maintenance_team',
            'request_type',
            'status',
            'assigned_to',
            'scheduled_date',
            'duration_hours',
        ]
        """
        🔍 EXPLANATION: fields
        Fields included in the form.
        Note: created_by is set automatically in the view.
        """
        
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Laptop won\'t turn on'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the issue or maintenance task...'
            }),
            'equipment': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_equipment'
            }),
            'maintenance_team': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_maintenance_team'
            }),
            'request_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_request_type'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'id': 'id_scheduled_date'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0',
                'placeholder': 'e.g., 2.5'
            }),
        }
        
        labels = {
            'subject': 'Subject',
            'description': 'Description',
            'equipment': 'Equipment',
            'maintenance_team': 'Maintenance Team',
            'request_type': 'Request Type',
            'status': 'Status',
            'assigned_to': 'Assigned To',
            'scheduled_date': 'Scheduled Date/Time',
            'duration_hours': 'Duration (hours)',
        }
        
        help_texts = {
            'equipment': 'Select the equipment that needs maintenance',
            'maintenance_team': 'Team responsible for this request (auto-filled from equipment)',
            'request_type': 'Corrective = Something broke. Preventive = Scheduled maintenance.',
            'scheduled_date': 'Required for Preventive requests. When should this be performed?',
            'duration_hours': 'Time taken to complete (fill when completed)',
        }
    
    def __init__(self, *args, **kwargs):
        """
        🔍 EXPLANATION: __init__ method
        Customizes form fields:
        - Filters equipment (only active, not scrapped)
        - Filters teams
        - Filters users (only active)
        - Sets default values
        """
        super().__init__(*args, **kwargs)
        
        # Filter equipment (only active, not scrapped)
        self.fields['equipment'].queryset = Equipment.objects.filter(
            is_scrapped=False
        ).order_by('name')
        self.fields['equipment'].empty_label = 'Select equipment...'
        
        # Filter maintenance teams
        self.fields['maintenance_team'].queryset = MaintenanceTeam.objects.all().order_by('name')
        self.fields['maintenance_team'].empty_label = 'Select team...'
        
        # Filter users (only active)
        from django.contrib.auth.models import User
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_to'].empty_label = 'Unassigned'
        
        # Make fields optional
        self.fields['description'].required = False
        self.fields['maintenance_team'].required = False
        self.fields['assigned_to'].required = False
        self.fields['scheduled_date'].required = False
        self.fields['duration_hours'].required = False
        
        # Set default status
        if not self.instance.pk:  # New request
            self.fields['status'].initial = 'New'
            self.fields['request_type'].initial = 'Corrective'
    
    def clean(self):
        """
        🔍 EXPLANATION: clean method
        Custom validation:
        - Preventive requests must have scheduled_date
        - Equipment must not be scrapped
        """
        cleaned_data = super().clean()
        request_type = cleaned_data.get('request_type')
        scheduled_date = cleaned_data.get('scheduled_date')
        equipment = cleaned_data.get('equipment')
        
        # Validate: Preventive requests must have scheduled_date
        if request_type == 'Preventive' and not scheduled_date:
            raise forms.ValidationError({
                'scheduled_date': 'Scheduled date is required for Preventive maintenance requests.'
            })
        
        # Validate: Equipment must not be scrapped
        if equipment and equipment.is_scrapped:
            raise forms.ValidationError({
                'equipment': 'Cannot create maintenance request for scrapped equipment.'
            })
        
        return cleaned_data


class StatusUpdateForm(forms.ModelForm):
    """
    Form for updating request status.
    
    🔍 EXPLANATION:
    Simplified form for quick status updates.
    Used in detail page for technicians to update status.
    """
    
    class Meta:
        model = MaintenanceRequest
        fields = ['status', 'assigned_to', 'duration_hours']
        
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0',
                'placeholder': 'e.g., 2.5'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter users (only active)
        from django.contrib.auth.models import User
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_to'].empty_label = 'Unassigned'
        self.fields['assigned_to'].required = False
        self.fields['duration_hours'].required = False

