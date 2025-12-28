"""
Views for teams app.

🔍 EXPLANATION:
These views handle maintenance team pages.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MaintenanceTeam


@login_required
def team_list(request):
    """
    List all maintenance teams.
    
    🔍 EXPLANATION:
    - Shows all teams in the system
    - Only accessible to logged-in users (@login_required)
    - Displays team members, active requests, and equipment counts
    """
    teams = MaintenanceTeam.objects.all().order_by('name')
    context = {
        'teams': teams,
    }
    return render(request, 'teams/list.html', context)


@login_required
def team_detail(request, pk):
    """
    Show details of a specific team.
    
    🔍 EXPLANATION:
    - pk = primary key (ID) of the team
    - Shows team members and assigned equipment
    - Shows team statistics
    """
    team = get_object_or_404(MaintenanceTeam, pk=pk)
    context = {
        'team': team,
    }
    return render(request, 'teams/detail.html', context)
