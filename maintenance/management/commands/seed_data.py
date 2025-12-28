"""
Management command to seed the database with sample data.

Usage:
    python manage.py seed_data

This creates:
    - Sample maintenance teams with members
    - Sample equipment categories
    - Sample equipment with various conditions
    - Sample users/technicians
    - Sample maintenance requests (various statuses, priorities, types)
    - Sample work orders
    - Sample activities
    - Sample maintenance sessions
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta, datetime, time as time_class
from teams.models import MaintenanceTeam
from equipment.models import Equipment, EquipmentCategory
from maintenance.models import MaintenanceRequest, WorkOrder, Activity, MaintenanceSession
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed the database with sample maintenance teams and equipment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed database with comprehensive data...'))
        
        # ========== CREATE USERS ==========
        self.stdout.write(self.style.SUCCESS('\n[1/7] Creating users and technicians...'))
        users_data = [
            {'username': 'admin', 'email': 'admin@gearguard.com', 'first_name': 'Admin', 'last_name': 'User', 'is_staff': True},
            {'username': 'john.doe', 'email': 'john@gearguard.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane.smith', 'email': 'jane@gearguard.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob.wilson', 'email': 'bob@gearguard.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
            {'username': 'alice.brown', 'email': 'alice@gearguard.com', 'first_name': 'Alice', 'last_name': 'Brown'},
            {'username': 'mike.jones', 'email': 'mike@gearguard.com', 'first_name': 'Mike', 'last_name': 'Jones'},
        ]
        
        created_users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')
                user.save()
                created_users[user_data['username']] = user
                self.stdout.write(self.style.SUCCESS(f'  [+] Created user: {user.get_full_name() or user.username}'))
            else:
                created_users[user_data['username']] = user
        
        # ========== CREATE EQUIPMENT CATEGORIES ==========
        self.stdout.write(self.style.SUCCESS('\n[2/7] Creating equipment categories...'))
        categories_data = [
            {'name': 'Computers', 'responsible': created_users.get('john.doe'), 'company': 'My Company (San Francisco)'},
            {'name': 'Software', 'responsible': created_users.get('jane.smith'), 'company': 'My Company (San Francisco)'},
            {'name': 'Monitors', 'responsible': created_users.get('bob.wilson'), 'company': 'My Company (San Francisco)'},
            {'name': 'Vehicles', 'responsible': created_users.get('mike.jones'), 'company': 'My Company (San Francisco)'},
            {'name': 'HVAC Systems', 'responsible': created_users.get('alice.brown'), 'company': 'My Company (San Francisco)'},
            {'name': 'Machinery', 'responsible': created_users.get('john.doe'), 'company': 'My Company (San Francisco)'},
        ]
        
        created_categories = {}
        for cat_data in categories_data:
            category, created = EquipmentCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            created_categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Created category: {category.name}'))
        
        # ========== CREATE MAINTENANCE TEAMS ==========
        self.stdout.write(self.style.SUCCESS('\n[3/7] Creating maintenance teams...'))
        teams_data = [
            {'name': 'IT Support Team', 'company': 'My Company (San Francisco)', 'members': ['john.doe', 'jane.smith']},
            {'name': 'Mechanics Team', 'company': 'My Company (San Francisco)', 'members': ['bob.wilson', 'mike.jones']},
            {'name': 'HVAC Team', 'company': 'My Company (San Francisco)', 'members': ['alice.brown']},
            {'name': 'Electrical Team', 'company': 'My Company (San Francisco)', 'members': ['bob.wilson']},
        ]
        
        created_teams = {}
        for team_data in teams_data:
            team, created = MaintenanceTeam.objects.get_or_create(
                name=team_data['name'],
                defaults={'company': team_data['company']}
            )
            # Add members
            for username in team_data['members']:
                if username in created_users:
                    team.members.add(created_users[username])
            created_teams[team_data['name']] = team
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Created team: {team.name}'))
        
        # ========== CREATE EQUIPMENT ==========
        self.stdout.write(self.style.SUCCESS('\n[4/7] Creating equipment...'))
        equipment_data = [
            # Equipment with Critical condition (will show in Critical Equipment stat)
            {
                'name': 'Critical Server #1', 'serial_number': 'SRV-CRIT-001', 'department': 'IT',
                'location': 'Building A, Server Room', 'category': 'Computers',
                'company': 'My Company (San Francisco)', 'used_for': 'Critical Data Storage',
                'condition': 'Critical', 'maintenance_team': 'IT Support Team',
                'assigned_employee': 'john.doe', 'acquisition_date': '2020-01-15',
            },
            {
                'name': 'Failing Production Line', 'serial_number': 'PROD-FAIL-001', 'department': 'Manufacturing',
                'location': 'Building B, Production Floor', 'category': 'Machinery',
                'company': 'My Company (San Francisco)', 'used_for': 'Production',
                'condition': 'Critical', 'maintenance_team': 'Mechanics Team',
                'acquisition_date': '2019-05-20',
            },
            {
                'name': 'Old Delivery Truck', 'serial_number': 'TRUCK-OLD-001', 'department': 'Operations',
                'location': 'Warehouse Parking', 'category': 'Vehicles',
                'company': 'My Company (San Francisco)', 'used_for': 'Delivery',
                'condition': 'Poor', 'maintenance_team': 'Mechanics Team',
                'acquisition_date': '2018-03-10',
            },
            {
                'name': 'Laptop #001', 'serial_number': 'LAP-001-2024', 'department': 'IT',
                'location': 'Building A, Floor 2, Room 205', 'category': 'Computers',
                'company': 'My Company (San Francisco)', 'used_for': 'Office Work',
                'condition': 'Good', 'maintenance_team': 'IT Support Team',
                'assigned_employee': 'john.doe', 'acquisition_date': '2024-01-15',
            },
            {
                'name': 'Laptop #002', 'serial_number': 'LAP-002-2024', 'department': 'IT',
                'location': 'Building A, Floor 2, Room 210', 'category': 'Computers',
                'company': 'My Company (San Francisco)', 'used_for': 'Development',
                'condition': 'Excellent', 'maintenance_team': 'IT Support Team',
                'assigned_employee': 'jane.smith', 'acquisition_date': '2024-02-20',
            },
            {
                'name': 'Printer Main Office', 'serial_number': 'PRT-MAIN-001', 'department': 'IT',
                'location': 'Building A, Floor 1, Reception', 'category': 'Machinery',
                'company': 'My Company (San Francisco)', 'used_for': 'Document Printing',
                'condition': 'Fair', 'maintenance_team': 'IT Support Team',
                'acquisition_date': '2023-06-10',
            },
            {
                'name': 'Delivery Van #1', 'serial_number': 'VAN-001', 'department': 'Operations',
                'location': 'Warehouse Parking', 'category': 'Vehicles',
                'company': 'My Company (San Francisco)', 'used_for': 'Delivery',
                'condition': 'Poor', 'maintenance_team': 'Mechanics Team',
                'acquisition_date': '2022-03-15',
            },
            {
                'name': 'AC Unit - Conference Room', 'serial_number': 'AC-CONF-001', 'department': 'Facilities',
                'location': 'Building A, Floor 3, Conference Room', 'category': 'HVAC Systems',
                'company': 'My Company (San Francisco)', 'used_for': 'Climate Control',
                'condition': 'Critical', 'maintenance_team': 'HVAC Team',
                'acquisition_date': '2021-08-20',
            },
            {
                'name': 'Production Machine #1', 'serial_number': 'MACH-PROD-001', 'department': 'Manufacturing',
                'location': 'Building B, Production Floor', 'category': 'Machinery',
                'company': 'My Company (San Francisco)', 'used_for': 'Production',
                'condition': 'Good', 'maintenance_team': 'Mechanics Team',
                'acquisition_date': '2023-11-05',
            },
            {
                'name': 'Server Rack #1', 'serial_number': 'SRV-001', 'department': 'IT',
                'location': 'Building A, Server Room', 'category': 'Computers',
                'company': 'My Company (San Francisco)', 'used_for': 'Data Storage',
                'condition': 'Excellent', 'maintenance_team': 'IT Support Team',
                'acquisition_date': '2024-03-10',
            },
            {
                'name': 'Forklift #1', 'serial_number': 'FL-001', 'department': 'Warehouse',
                'location': 'Warehouse Floor', 'category': 'Vehicles',
                'company': 'My Company (San Francisco)', 'used_for': 'Material Handling',
                'condition': 'Fair', 'maintenance_team': 'Mechanics Team',
                'acquisition_date': '2023-09-12',
            },
            # Equipment that will have multiple active requests (to show as critical)
            {
                'name': 'Problematic Machine #1', 'serial_number': 'MACH-PROB-001', 'department': 'Manufacturing',
                'location': 'Building B, Production Floor', 'category': 'Machinery',
                'company': 'My Company (San Francisco)', 'used_for': 'Production',
                'condition': 'Fair', 'maintenance_team': 'Mechanics Team',
                'acquisition_date': '2022-11-15',
            },
            {
                'name': 'Network Switch Main', 'serial_number': 'NET-SW-001', 'department': 'IT',
                'location': 'Building A, Server Room', 'category': 'Computers',
                'company': 'My Company (San Francisco)', 'used_for': 'Network Infrastructure',
                'condition': 'Good', 'maintenance_team': 'IT Support Team',
                'acquisition_date': '2023-04-20',
            },
        ]
        
        created_equipment = []
        for eq_data in equipment_data:
            equipment, created = Equipment.objects.get_or_create(
                serial_number=eq_data['serial_number'],
                defaults={
                    'name': eq_data['name'],
                    'department': eq_data['department'],
                    'location': eq_data['location'],
                    'category': created_categories.get(eq_data['category']),
                    'company': eq_data['company'],
                    'used_for': eq_data['used_for'],
                    'condition': eq_data['condition'],
                    'maintenance_team': created_teams.get(eq_data['maintenance_team']),
                    'assigned_employee': created_users.get(eq_data.get('assigned_employee')),
                    'acquisition_date': eq_data.get('acquisition_date'),
                }
            )
            if created:
                created_equipment.append(equipment)
                self.stdout.write(self.style.SUCCESS(f'  [+] Created equipment: {equipment.name}'))
        
        # ========== CREATE MAINTENANCE REQUESTS ==========
        self.stdout.write(self.style.SUCCESS('\n[5/7] Creating maintenance requests...'))
        
        # Get some equipment for requests
        equipment_list = list(Equipment.objects.all())
        if not equipment_list:
            self.stdout.write(self.style.ERROR('  [!] No equipment available. Please create equipment first.'))
            return
        
        # Get critical equipment for multiple active requests (to show in Critical Equipment stat)
        critical_equipment = Equipment.objects.filter(condition='Critical').first()
        poor_equipment = Equipment.objects.filter(condition='Poor').first()
        
        # Create requests with various statuses and priorities
        # Focus on creating ACTIVE requests (New/In Progress) to affect Open Requests stat
        requests_data = [
            # ACTIVE REQUESTS (New/In Progress) - These affect Open Requests and Technician Load
            {
                'subject': 'Critical server overheating', 'equipment': critical_equipment if critical_equipment else equipment_list[0],
                'request_type': 'Corrective', 'status': 'New', 'priority': 'Critical',
                'due_date': timezone.now() + timedelta(hours=2),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Server backup failed', 'equipment': critical_equipment if critical_equipment else equipment_list[0],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'High',
                'assigned_to': created_users.get('john.doe'),
                'due_date': timezone.now() + timedelta(hours=6),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Production line emergency stop', 'equipment': poor_equipment if poor_equipment else equipment_list[5],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'Critical',
                'assigned_to': created_users.get('bob.wilson'),
                'due_date': timezone.now() + timedelta(hours=1),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Truck engine warning light', 'equipment': poor_equipment if poor_equipment else equipment_list[3],
                'request_type': 'Corrective', 'status': 'New', 'priority': 'High',
                'due_date': timezone.now() + timedelta(days=1),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'AC unit not cooling', 'equipment': equipment_list[4],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'High',
                'assigned_to': created_users.get('alice.brown'),
                'due_date': timezone.now() + timedelta(hours=4),
                'created_by': created_users.get('john.doe'),
            },
            {
                'subject': 'Network switch malfunction', 'equipment': equipment_list[0],
                'request_type': 'Corrective', 'status': 'New', 'priority': 'Medium',
                'due_date': timezone.now() + timedelta(days=2),
                'created_by': created_users.get('jane.smith'),
            },
            {
                'subject': 'Forklift brake issue', 'equipment': equipment_list[7] if len(equipment_list) > 7 else equipment_list[0],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'High',
                'assigned_to': created_users.get('mike.jones'),
                'due_date': timezone.now() + timedelta(hours=3),
                'created_by': created_users.get('bob.wilson'),
            },
            # OVERDUE PREVENTIVE REQUESTS - These affect Overdue Requests stat
            {
                'subject': 'Overdue monthly inspection', 'equipment': equipment_list[2],
                'request_type': 'Preventive', 'status': 'New', 'priority': 'Medium',
                'scheduled_date': timezone.now() - timedelta(days=5),  # Overdue!
                'due_date': timezone.now() - timedelta(days=3),  # Overdue!
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Overdue quarterly maintenance', 'equipment': equipment_list[5],
                'request_type': 'Preventive', 'status': 'In Progress', 'priority': 'High',
                'scheduled_date': timezone.now() - timedelta(days=10),  # Overdue!
                'due_date': timezone.now() - timedelta(days=7),  # Overdue!
                'assigned_to': created_users.get('bob.wilson'),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Overdue AC filter replacement', 'equipment': equipment_list[4],
                'request_type': 'Preventive', 'status': 'New', 'priority': 'Medium',
                'scheduled_date': timezone.now() - timedelta(days=15),  # Overdue!
                'due_date': timezone.now() - timedelta(days=12),  # Overdue!
                'created_by': created_users.get('admin'),
            },
            # Multiple active requests for same equipment (to make it critical)
            {
                'subject': 'Machine overheating issue', 'equipment': Equipment.objects.filter(name__icontains='Problematic').first() or equipment_list[5],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'High',
                'assigned_to': created_users.get('bob.wilson'),
                'due_date': timezone.now() + timedelta(hours=8),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Machine calibration needed', 'equipment': Equipment.objects.filter(name__icontains='Problematic').first() or equipment_list[5],
                'request_type': 'Corrective', 'status': 'New', 'priority': 'Medium',
                'due_date': timezone.now() + timedelta(days=1),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Machine safety check', 'equipment': Equipment.objects.filter(name__icontains='Problematic').first() or equipment_list[5],
                'request_type': 'Preventive', 'status': 'In Progress', 'priority': 'High',
                'assigned_to': created_users.get('bob.wilson'),
                'scheduled_date': timezone.now() - timedelta(days=2),
                'due_date': timezone.now() - timedelta(days=1),
                'created_by': created_users.get('admin'),
            },
            # More active requests to increase technician load
            {
                'subject': 'Network connectivity issues', 'equipment': Equipment.objects.filter(name__icontains='Network').first() or equipment_list[0],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'High',
                'assigned_to': created_users.get('john.doe'),
                'due_date': timezone.now() + timedelta(hours=5),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Switch firmware update', 'equipment': Equipment.objects.filter(name__icontains='Network').first() or equipment_list[0],
                'request_type': 'Preventive', 'status': 'New', 'priority': 'Medium',
                'scheduled_date': timezone.now() + timedelta(days=3),
                'due_date': timezone.now() + timedelta(days=3),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Laptop keyboard not working', 'equipment': equipment_list[1],
                'request_type': 'Corrective', 'status': 'New', 'priority': 'Medium',
                'due_date': timezone.now() + timedelta(days=2),
                'created_by': created_users.get('jane.smith'),
            },
            {
                'subject': 'Printer paper jam', 'equipment': equipment_list[2],
                'request_type': 'Corrective', 'status': 'In Progress', 'priority': 'Low',
                'assigned_to': created_users.get('jane.smith'),
                'due_date': timezone.now() + timedelta(days=1),
                'created_by': created_users.get('admin'),
            },
            # FUTURE PREVENTIVE REQUESTS (not overdue)
            {
                'subject': 'Monthly printer maintenance', 'equipment': equipment_list[2],
                'request_type': 'Preventive', 'status': 'In Progress', 'priority': 'Medium',
                'scheduled_date': timezone.now() + timedelta(days=2),
                'due_date': timezone.now() + timedelta(days=2),
                'assigned_to': created_users.get('jane.smith'),
                'created_by': created_users.get('admin'),
            },
            {
                'subject': 'Server backup verification', 'equipment': equipment_list[6] if len(equipment_list) > 6 else equipment_list[0],
                'request_type': 'Preventive', 'status': 'New', 'priority': 'Low',
                'scheduled_date': timezone.now() + timedelta(days=7),
                'due_date': timezone.now() + timedelta(days=7),
                'created_by': created_users.get('admin'),
            },
            # COMPLETED REQUESTS (for history)
            {
                'subject': 'Van engine check', 'equipment': equipment_list[3],
                'request_type': 'Preventive', 'status': 'Repaired', 'priority': 'Medium',
                'scheduled_date': timezone.now() - timedelta(days=5),
                'assigned_to': created_users.get('bob.wilson'),
                'created_by': created_users.get('admin'),
                'completed_at': timezone.now() - timedelta(days=1),
                'duration_hours': 2.5,
            },
            {
                'subject': 'Production machine calibration', 'equipment': equipment_list[5],
                'request_type': 'Preventive', 'status': 'Repaired', 'priority': 'Medium',
                'scheduled_date': timezone.now() - timedelta(days=10),
                'assigned_to': created_users.get('bob.wilson'),
                'created_by': created_users.get('admin'),
                'completed_at': timezone.now() - timedelta(days=8),
                'duration_hours': 4.0,
            },
            {
                'subject': 'Laptop screen replacement', 'equipment': equipment_list[1],
                'request_type': 'Corrective', 'status': 'Repaired', 'priority': 'Medium',
                'assigned_to': created_users.get('jane.smith'),
                'created_by': created_users.get('jane.smith'),
                'completed_at': timezone.now() - timedelta(days=2),
                'duration_hours': 1.5,
            },
        ]
        
        created_requests = []
        for req_data in requests_data:
            # Auto-fill maintenance team from equipment
            if req_data['equipment'].maintenance_team:
                req_data['maintenance_team'] = req_data['equipment'].maintenance_team
            
            request = MaintenanceRequest.objects.create(**req_data)
            created_requests.append(request)
            self.stdout.write(self.style.SUCCESS(f'  [+] Created request: {request.subject}'))
        
        # ========== CREATE WORK ORDERS ==========
        self.stdout.write(self.style.SUCCESS('\n[6/7] Creating work orders...'))
        
        # Create work orders for some requests
        work_orders_data = [
            {
                'equipment': equipment_list[2],
                'maintenance_request': created_requests[1],
                'date': (timezone.now() + timedelta(days=2)).date(),
                'time': time_class(10, 0),
                'status': 'Open',
                'priority': 'Medium',
                'assigned_to': created_users.get('jane.smith'),
                'description': 'Monthly maintenance check for printer',
            },
            {
                'equipment': equipment_list[4],
                'maintenance_request': created_requests[2],
                'date': timezone.now().date(),
                'time': time_class(14, 0),
                'status': 'In Progress',
                'priority': 'Critical',
                'assigned_to': created_users.get('alice.brown'),
                'description': 'Fix AC unit noise issue',
            },
            {
                'equipment': equipment_list[7],
                'maintenance_request': created_requests[5],
                'date': timezone.now().date(),
                'time': time_class(9, 0),
                'status': 'In Progress',
                'priority': 'High',
                'assigned_to': created_users.get('mike.jones'),
                'description': 'Repair forklift hydraulic system',
            },
        ]
        
        created_work_orders = []
        for wo_data in work_orders_data:
            work_order = WorkOrder.objects.create(**wo_data)
            created_work_orders.append(work_order)
            self.stdout.write(self.style.SUCCESS(f'  [+] Created work order: {work_order.work_order_number}'))
        
        # ========== CREATE ACTIVITIES AND SESSIONS ==========
        self.stdout.write(self.style.SUCCESS('\n[7/7] Creating activities and maintenance sessions...'))
        
        # Create activities for work orders
        if created_work_orders:
            activities_data = [
                {
                    'work_order': created_work_orders[1],
                    'activity_type': 'Repair',
                    'description': 'Inspected AC unit, found loose fan blade',
                    'start_time': timezone.now() - timedelta(hours=2),
                    'end_time': timezone.now() - timedelta(hours=1),
                    'cost': 150.00,
                    'parts_used': 'Fan blade, screws',
                    'notes': 'Replaced fan blade and tightened all connections',
                },
                {
                    'work_order': created_work_orders[2],
                    'activity_type': 'Inspection',
                    'description': 'Initial inspection of hydraulic system',
                    'start_time': timezone.now() - timedelta(hours=3),
                    'end_time': timezone.now() - timedelta(hours=2, minutes=30),
                    'cost': 75.00,
                    'parts_used': 'Hydraulic fluid',
                    'notes': 'Found leak in hydraulic line',
                },
            ]
            
            for act_data in activities_data:
                activity = Activity.objects.create(**act_data)
                self.stdout.write(self.style.SUCCESS(f'  [+] Created activity: {activity.get_activity_type_display()}'))
            
            # Create maintenance sessions
            sessions_data = [
                {
                    'work_order': created_work_orders[1],
                    'date': timezone.now().date(),
                    'start_time': time_class(14, 0),
                    'end_time': time_class(15, 0),
                    'cost_per_hour': 50.00,
                    'duration_hours': 1.0,
                    'notes': 'AC unit repair session',
                },
                {
                    'work_order': created_work_orders[2],
                    'date': timezone.now().date(),
                    'start_time': time_class(9, 0),
                    'end_time': time_class(10, 30),
                    'cost_per_hour': 45.00,
                    'duration_hours': 1.5,
                    'notes': 'Forklift inspection and repair',
                },
            ]
            
            for sess_data in sessions_data:
                session = MaintenanceSession.objects.create(**sess_data)
                self.stdout.write(self.style.SUCCESS(f'  [+] Created session: {session.date} - ${session.total_cost}'))
        
        # ========== SUMMARY ==========
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('[+] Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'\nStatistics:'))
        self.stdout.write(self.style.SUCCESS(f'  - Users: {User.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Teams: {MaintenanceTeam.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Equipment Categories: {EquipmentCategory.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Equipment: {Equipment.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Maintenance Requests: {MaintenanceRequest.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Work Orders: {WorkOrder.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Activities: {Activity.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'  - Maintenance Sessions: {MaintenanceSession.objects.count()} total'))
        self.stdout.write(self.style.SUCCESS(f'\nRequest Status Breakdown:'))
        for status, count in MaintenanceRequest.objects.values('status').annotate(count=Count('id')).values_list('status', 'count'):
            self.stdout.write(self.style.SUCCESS(f'  - {status}: {count}'))
        self.stdout.write(self.style.SUCCESS(f'\n[+] Dashboard statistics should now show meaningful data!'))
        self.stdout.write(self.style.SUCCESS(f'[+] All reports and analysis features are ready to use!'))

