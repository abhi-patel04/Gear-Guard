"""
Signals for maintenance app.

🔍 EXPLANATION FOR BEGINNERS:
Django signals allow you to execute code when certain events happen.
Think of them as "hooks" that run automatically.

Examples:
- When a request is saved → Auto-assign team
- When status changes to "Scrap" → Mark equipment as scrapped
- When status changes to "Repaired" → Set completed_at

Benefits:
- Automation without manual intervention
- Consistent behavior
- Reduces errors
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import MaintenanceRequest


@receiver(pre_save, sender=MaintenanceRequest)
def auto_assign_team(sender, instance, **kwargs):
    """
    🔍 EXPLANATION: Auto-Assign Team Signal
    Automatically assigns maintenance team from equipment when request is created.
    
    How it works:
    1. Before saving request, check if team is not set
    2. If equipment has a maintenance team, use it
    3. This happens automatically - no manual intervention needed
    
    Example:
    - User creates request for "Laptop #123"
    - "Laptop #123" belongs to "IT Support Team"
    - System automatically sets request.maintenance_team = "IT Support Team"
    """
    # Only auto-assign if team is not already set
    if not instance.maintenance_team and instance.equipment:
        if instance.equipment.maintenance_team:
            instance.maintenance_team = instance.equipment.maintenance_team


@receiver(pre_save, sender=MaintenanceRequest)
def auto_set_completed_at(sender, instance, **kwargs):
    """
    🔍 EXPLANATION: Auto-Set Completed At Signal
    Automatically sets completed_at when status changes to "Repaired".
    
    How it works:
    1. Before saving, check if status is "Repaired"
    2. If status changed from something else to "Repaired"
    3. Set completed_at to current time
    
    Example:
    - Request status changes from "In Progress" to "Repaired"
    - System automatically sets completed_at = now()
    - Tracks when work was completed
    """
    # Only set if status is "Repaired" and it's a new status change
    if instance.status == 'Repaired':
        # Check if this is a status change (not initial creation)
        if instance.pk:  # Request already exists
            try:
                old_instance = MaintenanceRequest.objects.get(pk=instance.pk)
                # Only set if status changed to "Repaired"
                if old_instance.status != 'Repaired' and not instance.completed_at:
                    instance.completed_at = timezone.now()
            except MaintenanceRequest.DoesNotExist:
                # New request with status "Repaired" (unlikely but possible)
                if not instance.completed_at:
                    instance.completed_at = timezone.now()
        else:
            # New request with status "Repaired" (unlikely but possible)
            if not instance.completed_at:
                instance.completed_at = timezone.now()


@receiver(post_save, sender=MaintenanceRequest)
def handle_scrap_status(sender, instance, created, **kwargs):
    """
    🔍 EXPLANATION: Scrap Logic Signal
    Automatically marks equipment as scrapped when request status is "Scrap".
    
    How it works:
    1. After saving request, check if status is "Scrap"
    2. If yes, mark the equipment as scrapped
    3. This prevents new requests for scrapped equipment
    
    Example:
    - Request status changes to "Scrap"
    - System automatically sets equipment.is_scrapped = True
    - Equipment can no longer have new maintenance requests
    
    Note: This uses post_save because we need the request to be saved first.
    """
    if instance.status == 'Scrap' and instance.equipment:
        # Mark equipment as scrapped
        instance.equipment.is_scrapped = True
        instance.equipment.save(update_fields=['is_scrapped'])


@receiver(post_save, sender=MaintenanceRequest)
def handle_repaired_status(sender, instance, created, **kwargs):
    """
    🔍 EXPLANATION: Repaired Status Signal
    Additional logic when request is marked as "Repaired".
    
    How it works:
    1. After saving request with status "Repaired"
    2. Can add additional logic here (notifications, reports, etc.)
    
    Example use cases:
    - Send notification to creator
    - Update equipment last_serviced date
    - Generate completion report
    """
    if instance.status == 'Repaired':
        # Future: Add notifications, reports, etc.
        pass

