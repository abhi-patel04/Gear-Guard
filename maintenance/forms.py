"""
Forms for maintenance app.

🔍 EXPLANATION FOR BEGINNERS:
Forms for creating and updating maintenance requests.
"""
from django import forms
from .models import MaintenanceRequest, WorkOrder, Activity, MaintenanceSession
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
            'priority',
            'assigned_to',
            'scheduled_date',
            'due_date',
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
            'request_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_assigned_to'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'id': 'id_scheduled_date'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
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
            'priority': 'Priority',
            'assigned_to': 'Assigned To',
            'scheduled_date': 'Scheduled Date/Time',
            'due_date': 'Due Date',
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
        - Filters users (only team members if team is selected)
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
        
        # Filter users based on team membership (workflow logic: only team members can pick up requests)
        from django.contrib.auth.models import User
        maintenance_team = None
        
        # Get team from instance (if editing) or initial data
        if self.instance and self.instance.pk:
            maintenance_team = self.instance.maintenance_team
        elif 'initial' in kwargs and 'maintenance_team' in kwargs['initial']:
            maintenance_team = kwargs['initial']['maintenance_team']
        
        # If team is selected, only show team members; otherwise show all active users
        if maintenance_team:
            self.fields['assigned_to'].queryset = maintenance_team.members.filter(is_active=True).order_by('username')
            self.fields['assigned_to'].help_text = f'Only team members of {maintenance_team.name} can be assigned'
        else:
            self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
            self.fields['assigned_to'].help_text = 'Select a team first to filter available technicians'
        
        self.fields['assigned_to'].empty_label = 'Unassigned'
        
        # Make fields optional
        self.fields['description'].required = False
        self.fields['maintenance_team'].required = False
        self.fields['assigned_to'].required = False
        self.fields['scheduled_date'].required = False
        self.fields['due_date'].required = False
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
        - Assigned technician must be a member of the selected team (workflow logic)
        """
        cleaned_data = super().clean()
        request_type = cleaned_data.get('request_type')
        scheduled_date = cleaned_data.get('scheduled_date')
        equipment = cleaned_data.get('equipment')
        maintenance_team = cleaned_data.get('maintenance_team')
        assigned_to = cleaned_data.get('assigned_to')
        
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
        
        # Validate: Workflow logic - assigned technician must be a member of the selected team
        if maintenance_team and assigned_to:
            if assigned_to not in maintenance_team.members.all():
                raise forms.ValidationError({
                    'assigned_to': f'The selected technician must be a member of {maintenance_team.name} team. Only team members can pick up requests for their team.'
                })
        
        return cleaned_data


class StatusUpdateForm(forms.ModelForm):
    """
    Form for updating request status.
    
    🔍 EXPLANATION:
    Simplified form for quick status updates.
    Used in detail page for technicians to update status.
    Implements workflow logic: only team members can be assigned.
    """
    
    class Meta:
        model = MaintenanceRequest
        fields = ['status', 'assigned_to', 'duration_hours']
        
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_status_assigned_to'
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
        
        # Filter users based on team membership (workflow logic: only team members can pick up requests)
        from django.contrib.auth.models import User
        
        # Get the maintenance team from the instance
        if self.instance and self.instance.maintenance_team:
            maintenance_team = self.instance.maintenance_team
            self.fields['assigned_to'].queryset = maintenance_team.members.filter(is_active=True).order_by('username')
            self.fields['assigned_to'].help_text = f'Only team members of {maintenance_team.name} can be assigned'
        else:
            self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
            self.fields['assigned_to'].help_text = 'No team assigned to this request'
        
        self.fields['assigned_to'].empty_label = 'Unassigned'
        self.fields['assigned_to'].required = False
        self.fields['duration_hours'].required = False
    
    def clean(self):
        """
        Validate that assigned technician is a team member.
        """
        cleaned_data = super().clean()
        assigned_to = cleaned_data.get('assigned_to')
        
        # Validate: Workflow logic - assigned technician must be a member of the team
        if self.instance.maintenance_team and assigned_to:
            if assigned_to not in self.instance.maintenance_team.members.all():
                raise forms.ValidationError({
                    'assigned_to': f'The selected technician must be a member of {self.instance.maintenance_team.name} team. Only team members can pick up requests for their team.'
                })
        
        return cleaned_data


class WorkOrderForm(forms.ModelForm):
    """Form for creating and editing Work Orders."""
    
    class Meta:
        model = WorkOrder
        fields = [
            'equipment',
            'maintenance_request',
            'date',
            'time',
            'status',
            'priority',
            'assigned_to',
            'description'
        ]
        
        widgets = {
            'equipment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'maintenance_request': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import User
        
        self.fields['equipment'].queryset = Equipment.objects.all().order_by('name')
        self.fields['equipment'].empty_label = 'Select equipment...'
        
        self.fields['maintenance_request'].queryset = MaintenanceRequest.objects.all().order_by('-created_at')
        self.fields['maintenance_request'].empty_label = 'None (optional)'
        self.fields['maintenance_request'].required = False
        
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_to'].empty_label = 'Unassigned'
        self.fields['assigned_to'].required = False
        
        self.fields['description'].required = False


class ActivityForm(forms.ModelForm):
    """Form for creating and editing Activities."""
    
    class Meta:
        model = Activity
        fields = [
            'activity_type',
            'description',
            'start_time',
            'end_time',
            'cost',
            'parts_used',
            'notes'
        ]
        
        widgets = {
            'activity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'parts_used': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_time'].required = False
        self.fields['cost'].required = False
        self.fields['parts_used'].required = False
        self.fields['notes'].required = False


class MaintenanceSessionForm(forms.ModelForm):
    """Form for creating and editing Maintenance Sessions."""
    
    class Meta:
        model = MaintenanceSession
        fields = [
            'date',
            'start_time',
            'end_time',
            'cost_per_hour',
            'duration_hours',
            'notes'
        ]
        
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'cost_per_hour': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g., 1.5'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_time'].required = False
        self.fields['notes'].required = False

