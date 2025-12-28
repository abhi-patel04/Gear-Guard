# 🛡️ GearGuard – The Ultimate Maintenance Tracker

## 📚 What is GearGuard?

**GearGuard** is a web-based maintenance management system that helps companies track and manage equipment maintenance.

### Real-World Problem It Solves

Imagine you work in a factory with 100 machines. When a machine breaks:
- ❌ **Without GearGuard**: You call maintenance, they write it on paper, you lose track, machines break again
- ✅ **With GearGuard**: You create a request online, it's assigned to a technician, tracked in a Kanban board, and scheduled on a calendar

### Who Uses It?

1. **👤 User (Regular Employee)**
   - Creates maintenance requests when something breaks
   - Views their own requests

2. **🔧 Technician**
   - Views requests assigned to their team
   - Updates request status (In Progress → Repaired)
   - Sees their work in a Kanban board

3. **👔 Manager**
   - Schedules preventive maintenance (before things break)
   - Assigns technicians to teams
   - Views reports and statistics

---

## 🧱 Tech Stack Explained

### Django 5+
**What it is**: A Python web framework (a toolkit for building websites)
**Why we use it**: 
- Handles database operations automatically
- Built-in admin panel
- Secure by default
- Great for beginners

### Django Templates
**What it is**: HTML files with special Django syntax
**Why we use it**: 
- Mix HTML with dynamic data
- Reusable components (like a header/footer)

### Bootstrap 5
**What it is**: A CSS framework (pre-made styles)
**Why we use it**: 
- Beautiful UI without writing custom CSS
- Responsive (works on mobile/tablet/desktop)
- Professional look instantly

### HTMX
**What it is**: JavaScript library for dynamic updates
**Why we use it**: 
- Update parts of a page without reloading
- Simpler than writing complex JavaScript
- Makes the Kanban board interactive

### SortableJS
**What it is**: JavaScript library for drag-and-drop
**Why we use it**: 
- Drag cards in the Kanban board
- Visual workflow management

### FullCalendar
**What it is**: JavaScript calendar widget
**Why we use it**: 
- Show preventive maintenance schedules
- Visual planning tool

### SQLite
**What it is**: A database (stores all your data)
**Why we use it**: 
- No setup required (file-based)
- Perfect for development
- Easy to backup (just copy the file)

### Django Auth + Groups
**What it is**: Django's built-in user system
**Why we use it**: 
- Login/logout functionality
- User roles (User, Technician, Manager)
- Permission management

---

## 📂 Project Structure Explained

```
gearguard/              ← Main project folder (Django project)
├── manage.py           ← Django's command-line tool
├── requirements.txt    ← List of Python packages needed
├── db.sqlite3          ← Database file (created after migrations)
├── gearguard/          ← Project settings folder
│   ├── settings.py     ← Configuration (apps, database, etc.)
│   ├── urls.py         ← Main URL routing
│   └── wsgi.py         ← Web server interface
│
├── accounts/           ← App: User authentication
│   ├── models.py       ← Database models (User profiles)
│   ├── views.py        ← Functions that handle requests
│   ├── urls.py         ← URL routes for this app
│   └── templates/      ← HTML files for this app
│
├── teams/              ← App: Maintenance teams
│   ├── models.py       ← MaintenanceTeam model
│   ├── views.py        ← Team management views
│   └── urls.py         ← Team URLs
│
├── equipment/          ← App: Equipment/assets
│   ├── models.py       ← Equipment model
│   ├── views.py        ← Equipment list, detail, create
│   └── urls.py         ← Equipment URLs
│
├── maintenance/        ← App: Maintenance requests
│   ├── models.py       ← MaintenanceRequest model
│   ├── views.py        ← Request creation, Kanban, Calendar
│   └── urls.py         ← Maintenance URLs
│
├── dashboard/          ← App: Dashboard/homepage
│   ├── views.py        ← Statistics and overview
│   └── urls.py         ← Dashboard URLs
│
├── templates/          ← Shared HTML templates
│   └── base.html       ← Base layout (header, sidebar, footer)
│
└── static/             ← CSS, JavaScript, images
    ├── css/
    ├── js/
    └── images/
```

### What is a "Project" vs "App"?

**Project** (`gearguard/`): The entire website
- Contains settings
- Connects all apps together
- One project can have many apps

**App** (`equipment/`, `maintenance/`, etc.): A feature/module
- Handles one specific functionality
- Can be reused in other projects
- Example: `equipment/` app handles all equipment-related features

---

## 🗄️ Database Models Explained

### Model 1: MaintenanceTeam
**Purpose**: Represents a group of technicians (e.g., "IT Support", "Mechanics")

**Fields**:
- `name`: Name of the team (e.g., "IT Support")
- `members`: Users belonging to this team (ManyToMany relationship)

**Used In**:
- Assigning equipment to a team
- Filtering which technician sees which request
- Kanban board visibility
- Calendar color grouping

### Model 2: Equipment
**Purpose**: Represents company assets (machines, laptops, vehicles)

**Fields**:
- `name`: Equipment name (e.g., "Laptop #123")
- `serial_number`: Unique identification
- `department`: Which department owns it
- `location`: Physical location
- `maintenance_team`: Which team handles it (ForeignKey)
- `assigned_employee`: Optional user who uses it
- `is_scrapped`: Whether equipment is unusable

**Used In**:
- Equipment list & detail UI
- Auto-assigning maintenance team to requests
- Smart "Maintenance" button
- Scrap logic (disable equipment)

### Model 3: MaintenanceRequest
**Purpose**: Represents a repair or maintenance job

**Fields**:
- `subject`: What is wrong
- `equipment`: Which equipment is affected (ForeignKey)
- `maintenance_team`: Auto-filled from equipment
- `request_type`: Corrective (breakdown) / Preventive (scheduled)
- `assigned_to`: Technician handling it
- `scheduled_date`: Only for Preventive requests
- `duration_hours`: Time taken to complete
- `status`: New / In Progress / Repaired / Scrap
- `created_by`: User who created request
- `created_at`: Auto timestamp

**Used In**:
- Request creation form
- Kanban board
- Request detail page
- Calendar view
- Dashboard statistics
- Automation logic

---

## 🔄 Workflows Explained

### Workflow 1: Corrective Maintenance (Breakdown)
**Scenario**: A machine breaks, user reports it

**Steps**:
1. User creates request → Selects equipment → System auto-fills maintenance team
2. Status = "New" → Appears in Kanban board
3. Technician assigns self → Status → "In Progress"
4. Technician enters duration → Status → "Repaired"
5. Request is complete

**Models Used**: Equipment, MaintenanceRequest, MaintenanceTeam

### Workflow 2: Preventive Maintenance
**Scenario**: Manager schedules regular maintenance

**Steps**:
1. Manager creates request → Selects "Preventive" type
2. Sets scheduled date → Request appears on Calendar
3. Technician performs task on scheduled date
4. Updates status to "Repaired"

**Models Used**: MaintenanceRequest, MaintenanceTeam

---

## 🚀 Getting Started

### Step 1: Install Dependencies
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate     # Mac/Linux

# Install packages
pip install -r requirements.txt
```

### Step 2: Run Migrations
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser
```bash
# Create admin account
python manage.py createsuperuser
```

### Step 4: Run Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/

---

## 📝 Development Order

We'll build in this order:
1. ✅ Project setup
2. ⏳ Models
3. ⏳ Admin panel
4. ⏳ Base UI layout
5. ⏳ Equipment module
6. ⏳ Maintenance module
7. ⏳ Kanban board
8. ⏳ Calendar view
9. ⏳ Automation
10. ⏳ Dashboard

---

## 🎨 UI/UX Rules

- **Light theme**: Easy on the eyes
- **Blue primary color**: Professional, trustworthy
- **Sidebar navigation**: Easy access to all features
- **Card-based UI**: Clean, organized information
- **Icons everywhere**: Visual cues for faster understanding
- **Kanban = visual workflow**: See work progress at a glance
- **Calendar = planning tool**: Schedule preventive maintenance

---

## 🔐 User Roles & Permissions

### User (Default)
- Can create maintenance requests
- Can view own requests
- Cannot assign technicians

### Technician
- Everything a User can do
- Can view requests assigned to their team
- Can update request status
- Can see Kanban board for their team

### Manager
- Everything a Technician can do
- Can schedule preventive maintenance
- Can assign technicians
- Can view reports
- Can manage equipment

---

## 🧪 Testing

After each step, test:
1. Can I access the page?
2. Does the form work?
3. Is data saved to database?
4. Do permissions work correctly?

---

## 📖 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [HTMX Documentation](https://htmx.org/)
- [FullCalendar Documentation](https://fullcalendar.io/docs)

---

## 🤝 Support

If you're stuck:
1. Check the error message
2. Read the model/field explanations above
3. Check Django documentation
4. Ask for help!

---

**Happy Coding! 🚀**

