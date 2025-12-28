lo# ✅ Step 2: Create Models - COMPLETE

## 📋 What Was Built

### 1. MaintenanceTeam Model (`teams/models.py`)
**Purpose**: Represents a group of technicians who work together.

**Fields**:
- `name` - Team name (e.g., "IT Support", "Mechanics")
- `members` - ManyToMany relationship with User (technicians in the team)
- `created_at` - When team was created
- `updated_at` - Last modification time

**Key Features**:
- ✅ ManyToMany relationship with User (one user can be in multiple teams)
- ✅ Custom methods: `get_member_count()`, `get_active_requests_count()`
- ✅ Alphabetical ordering by name

**Used In**:
- Equipment assignment (equipment belongs to a team)
- Request filtering (technicians see only their team's requests)
- Kanban board (filter by team)
- Calendar view (color grouping by team)

---

### 2. Equipment Model (`equipment/models.py`)
**Purpose**: Represents physical assets that need maintenance.

**Fields**:
- `name` - Equipment name (e.g., "Laptop #123")
- `serial_number` - Unique identification (optional)
- `department` - Department that owns it
- `location` - Physical location
- `maintenance_team` - ForeignKey to MaintenanceTeam (which team handles it)
- `assigned_employee` - ForeignKey to User (who uses it, optional)
- `is_scrapped` - Boolean (if True, equipment is unusable)
- `created_at` - When equipment was added
- `updated_at` - Last modification time

**Key Features**:
- ✅ ForeignKey to MaintenanceTeam (auto-assigns team to requests)
- ✅ ForeignKey to User (track who uses equipment)
- ✅ Custom methods: `get_active_requests_count()`, `can_create_request()`
- ✅ Scrap logic (prevents new requests for scrapped equipment)

**Used In**:
- Equipment list & detail pages
- Auto-assigning maintenance team to requests (AUTOMATION)
- Smart "Maintenance" button (shows only requests for this equipment)
- Scrap logic (disable equipment when status = "Scrap")

---

### 3. MaintenanceRequest Model (`maintenance/models.py`)
**Purpose**: Represents a maintenance job (corrective or preventive).

**Fields**:
- `subject` - Brief description of the issue
- `description` - Detailed description (optional)
- `equipment` - ForeignKey to Equipment (which equipment needs maintenance)
- `maintenance_team` - ForeignKey to MaintenanceTeam (auto-filled from equipment)
- `request_type` - Choice: "Corrective" or "Preventive"
- `status` - Choice: "New", "In Progress", "Repaired", "Scrap"
- `assigned_to` - ForeignKey to User (technician handling it, optional)
- `scheduled_date` - DateTime (only for Preventive, appears on calendar)
- `duration_hours` - Decimal (time taken to complete)
- `completed_at` - DateTime (when request was completed)
- `created_by` - ForeignKey to User (who created the request)
- `created_at` - When request was created
- `updated_at` - Last modification time

**Key Features**:
- ✅ ForeignKey to Equipment (links request to equipment)
- ✅ ForeignKey to MaintenanceTeam (auto-filled from equipment)
- ✅ Choice fields for status and request_type
- ✅ Custom methods: `is_overdue()`, `mark_completed()`, `get_duration_display()`
- ✅ Overdue detection logic (for preventive maintenance)

**Used In**:
- Request creation form
- Kanban board (columns match status values)
- Calendar view (shows preventive maintenance)
- Dashboard statistics (open requests, overdue requests)
- Request detail page
- Automation logic (scrap equipment, auto-assign team)

---

## 🔍 Key Concepts Explained

### What is a Model?
A **model** is a Python class that represents a database table.
- Each model class = one database table
- Each field = one column in the table
- Each instance = one row in the table

**Example**:
```python
class Equipment(models.Model):
    name = models.CharField(max_length=200)
```
- Creates table: `equipment_equipment`
- Creates column: `name` (VARCHAR(200))
- Each Equipment object = one row in the table

---

### What is a ForeignKey?
A **ForeignKey** creates a relationship between two models.

**Example**:
```python
equipment = models.ForeignKey(Equipment, ...)
```
- One request belongs to ONE equipment
- One equipment can have MANY requests
- This is a "one-to-many" relationship

**Real-World Example**:
- "Laptop #123" (Equipment) can have 5 maintenance requests
- Each request belongs to "Laptop #123"

---

### What is a ManyToManyField?
A **ManyToManyField** creates a many-to-many relationship.

**Example**:
```python
members = models.ManyToManyField(User, ...)
```
- One user can be in MULTIPLE teams
- One team can have MULTIPLE users
- This is a "many-to-many" relationship

**Real-World Example**:
- John (User) can be in "IT Support" AND "Weekend On-Call" teams
- "IT Support" team has John, Jane, and Bob

---

### What are Choices?
**Choices** limit a field to specific values.

**Example**:
```python
STATUS_CHOICES = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Repaired', 'Repaired'),
]
status = models.CharField(choices=STATUS_CHOICES)
```
- Status can ONLY be: "New", "In Progress", or "Repaired"
- Prevents invalid values (like "Pending" or "Done")
- Used in forms (dropdown menu)

---

### What are Custom Methods?
**Custom methods** are functions you write to add functionality to models.

**Example**:
```python
def is_overdue(self):
    if self.scheduled_date < timezone.now():
        return True
    return False
```
- Can be called on any MaintenanceRequest object
- Example: `request.is_overdue()` returns True/False
- Used in templates, views, and logic

---

## 🔄 Model Relationships Diagram

```
User (Django built-in)
  ↑
  │ ManyToMany
  │
MaintenanceTeam
  ↑
  │ ForeignKey
  │
Equipment ────┐
              │ ForeignKey
              │
              MaintenanceRequest
              │
              │ ForeignKey
              │
              User (assigned_to, created_by)
```

**Explanation**:
- Equipment → MaintenanceTeam (one-to-many)
- MaintenanceRequest → Equipment (many-to-one)
- MaintenanceRequest → MaintenanceTeam (many-to-one)
- MaintenanceTeam → User (many-to-many)
- MaintenanceRequest → User (many-to-one, for assigned_to and created_by)

---

## 🤖 Automation Logic (Prepared)

### 1. Auto-Assign Team
**How it works**:
- User selects equipment in request form
- System automatically fills: `request.maintenance_team = equipment.maintenance_team`
- **Implementation**: Will be done in forms/views (Step 7)

### 2. Overdue Detection
**How it works**:
- Method: `request.is_overdue()`
- Checks: If `scheduled_date < today` AND `status != "Repaired"`
- **Implementation**: Already implemented in model!

### 3. Scrap Logic
**How it works**:
- When request status = "Scrap"
- System sets: `equipment.is_scrapped = True`
- **Implementation**: Will be done with Django signals (Step 10)

---

## 🧪 How to Test

### Step 1: Open Django Shell
```bash
python manage.py shell
```

### Step 2: Test Creating a Team
```python
from teams.models import MaintenanceTeam
from django.contrib.auth.models import User

# Create a team
team = MaintenanceTeam.objects.create(name="IT Support")
print(team)  # Should print: "IT Support"
print(team.get_member_count())  # Should print: 0
```

### Step 3: Test Creating Equipment
```python
from equipment.models import Equipment

# Create equipment
equipment = Equipment.objects.create(
    name="Laptop #123",
    department="IT",
    location="Building A, Room 205",
    maintenance_team=team
)
print(equipment)  # Should print: "Laptop #123 (IT)"
```

### Step 4: Test Creating a Request
```python
from maintenance.models import MaintenanceRequest

# Create a request
request = MaintenanceRequest.objects.create(
    subject="Laptop won't turn on",
    equipment=equipment,
    maintenance_team=team,
    request_type="Corrective",
    status="New",
    created_by=User.objects.first()  # Use first user if exists
)
print(request)  # Should print: "Laptop won't turn on - New"
print(request.is_overdue())  # Should print: False
```

### Step 5: Test Relationships
```python
# Get all requests for equipment
print(equipment.maintenance_requests.all())

# Get all equipment for team
print(team.equipment.all())

# Get active requests count
print(team.get_active_requests_count())
```

---

## 📊 Database Tables Created

After running migrations, these tables were created:

1. **teams_maintenanceteam**
   - id, name, created_at, updated_at

2. **teams_maintenanceteam_members** (ManyToMany table)
   - id, maintenanceteam_id, user_id

3. **equipment_equipment**
   - id, name, serial_number, department, location, maintenance_team_id, assigned_employee_id, is_scrapped, created_at, updated_at

4. **maintenance_maintenancerequest**
   - id, subject, description, equipment_id, maintenance_team_id, request_type, status, assigned_to_id, scheduled_date, duration_hours, completed_at, created_by_id, created_at, updated_at

---

## ✅ What's Working

1. ✅ All three models created with comprehensive explanations
2. ✅ All relationships defined (ForeignKey, ManyToMany)
3. ✅ Choice fields for status and request_type
4. ✅ Custom methods for business logic
5. ✅ Migrations created and applied
6. ✅ Database tables created
7. ✅ No errors in Django check

---

## ⏭️ Next Steps

**Step 3: Set up Django Admin Panel** (Coming Next)
- Register all models in admin
- Customize admin interface
- Add filters, search, and list displays
- Test creating data through admin

---

## 🎓 Learning Points

1. **Models = Database Tables**
   - Each model class = one table
   - Each field = one column

2. **Relationships**
   - ForeignKey = one-to-many
   - ManyToMany = many-to-many

3. **Choices**
   - Limit field values
   - Used in forms (dropdowns)

4. **Custom Methods**
   - Add functionality to models
   - Can be called on instances

5. **Migrations**
   - Create database tables
   - Track database changes
   - Version control for database

---

## 🐛 Troubleshooting

### Error: "No module named 'teams.models'"
**Solution**: Make sure all apps are in `INSTALLED_APPS` in `settings.py`

### Error: "Circular import"
**Solution**: Use string references in ForeignKey: `ForeignKey('teams.MaintenanceTeam')`

### Error: "Field 'x' doesn't have a default value"
**Solution**: Add `default=...` or `null=True, blank=True` to the field

---

**✅ Step 2 Complete! Ready for Step 3: Admin Panel**

