readme_content = """# Django Application – Alert Management

##  Description

A Django web application for managing alerts in a logistics environment.
The application allows users to create, track, and manage alerts related to stock levels and kit zones.

---

##  Architecture

### Project Structure

mon_projet/
├── manage.py
├── requirements.txt
├── README.md
├── check_app.py
├── mon_projet/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── authentication/     # User management
│   ├── alertes/            # Alert management
│   └── dashboard/          # Dashboard
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── registration/
    ├── alertes/
    └── dashboard/

---

### Django Applications

#### 1. Authentication
- **Models:** CustomUser with roles (admin, agent_kit, agent_cross, agent_debord)
- **Views:** Register, login, logout
- **Features:** Custom authentication with role-based access

#### 2. Alerts
- **Models:** Alert, AlertHistory, OverflowStock
- **Views:** Create, list, update status
- **Features:** Complete lifecycle management of alerts

#### 3. Dashboard
- **Views:** Overview with key metrics
- **Features:** Real-time summary of alerts and statistics

---

##  Installation & Configuration

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or MariaDB
- pip (Python package manager)

### 1. Install Dependencies
pip install -r requirements.txt

### 2. Database Configuration

#### Option A: MySQL (Recommended for production)
1. Create a MySQL database:
CREATE DATABASE alert_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON alert_management_db.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;

2. Update your settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alert_management_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

#### Option B: SQLite (For development)
Uncomment the SQLite section in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

### 3. Run Database Migrations
python manage.py makemigrations
python manage.py migrate

### 4. Create a Superuser
python manage.py createsuperuser

### 5. Verify Installation
python check_app.py

### 6. Start the Development Server
python manage.py runserver

Access the app at: http://127.0.0.1:8000/

---

##  Usage

### User Roles
1. **Administrator:** Full access to all features
2. **Kit Area Agent:** Creates and manages kit-related alerts
3. **Cross Dock Agent:** Manages transfers and deliveries
4. **Overflow Agent:** Manages overflow stock

### Main Features

#### 1. Dashboard
- Overview of alerts by status
- Real-time metrics
- Recent alerts
- Zone-based statistics

#### 2. Alert Management
- **Create:** New alert with reference, zone, and bin count
- **Track:** Full modification history
- **Status Flow:** In Progress → Delivered → FLC Sent → Closed
- **Filters:** By status, zone, or date

#### 3. Authentication
- Secure login
- Role-based registration
- Session management

---

## 🔧 Advanced Configuration

### Environment Variables
Create a .env file for sensitive data:
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=alert_management_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

### Security
- CSRF protection enabled
- XSS protection
- Authentication required for all views
- Client & server-side form validation

### Performance
- Auto-refresh dashboard (every 30s)
- Optimized queries with select_related
- Pagination for long lists
- Metric caching

---

##  User Interface

### Frontend Technologies
- **Bootstrap 5** – Responsive CSS framework
- **Font Awesome** – Icons
- **jQuery** – JavaScript interactions
- **AJAX** – Real-time updates

### UI Features
- Fully responsive (mobile-friendly)
- Real-time notifications
- Confirmation dialogs for critical actions
- Loading indicators
- Table sorting & filtering

---

##  Database

### Main Models

#### CustomUser
- username, email, password (inherited from AbstractUser)
- role: Choice among the 4 roles
- phone: Optional phone number
- created_at: Creation date

#### Alert
- reference: Unique reference
- zone_kit: Kit zone (1–11)
- bin_count: Number of remaining bins
- status: in_progress, delivered, flc, closed
- created_at, closed_at
- created_by, handled_by: Foreign keys to CustomUser
- comments: Text field

#### AlertHistory
- alert: Foreign key to Alert
- action: Description of action
- user: Who performed it
- modified_at: Date/time
- old_status, new_status: Status transitions

---

##  Testing & Verification

### Verification Script
python check_app.py

This script checks:
- ✅ Django configuration
- ✅ Models & relationships
- ✅ Views & URLs
- ✅ Templates & static files
- ✅ Database connection

### Unit Tests
python manage.py test

---

##  Deployment

### Preparing for Production
1. Set DEBUG = False in settings.py
2. Configure ALLOWED_HOSTS
3. Use a robust DB (MySQL/PostgreSQL)
4. Run collectstatic for static files
5. Use a production web server (Nginx + Gunicorn)

### Production Settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

---

##  API & Extensions

### Main URLs
- `/` – Dashboard
- `/auth/login/` – Login
- `/auth/register/` – Register
- `/alertes/create/` – Create alert
- `/alertes/list/` – List alerts
- `/alertes/update-status/<id>/` – AJAX status update

### Possible Extensions
- REST API with Django REST Framework
- Email/SMS notifications
- Excel/PDF export
- Advanced charts with Chart.js
- Integration with external systems

---

##  Troubleshooting

### Common Issues
1. **MySQL Connection Error**
   - Ensure MySQL is running
   - Check credentials
   - Verify user permissions

2. **Migration Error**
   python manage.py makemigrations --empty apps.authentication
   python manage.py migrate --fake-initial

3. **Static Files Not Found**
   python manage.py collectstatic

4. **CSRF Error**
   - Ensure {% csrf_token %} is in forms
   - Check CSRF settings in settings.py



**Version:** 1.0.0
**Last Updated:** December 2024
**Compatibility:** Django 4.2+, Python 3.8+
"""
