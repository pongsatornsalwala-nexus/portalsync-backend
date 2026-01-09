# PortalSync Backend

Django REST API backend for PortalSync - HR Automation System for Social Security Fund (SSF) and AIA Group Insurance registration tracking.

## 🚀 Features

- Employee management with benefit tracking
- Worksite configuration
- SSF and AIA queue management
- Dashboard statistics API
- Django Admin interface

## 🛠️ Tech Stack

- Django 6.0
- Django REST Framework 3.16
- PostgreSQL
- Python 3.13

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/portalsync-backend.git
cd portalsync-backend
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database
```bash
createdb portalsync_db
```

5. Configure environment
```bash
# Update config/settings.py with your database credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portalsync_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

6. Run migrations
```bash
python manage.py migrate
```

7. Create superuser
```bash
python manage.py createsuperuser
```

8. Run development server
```bash
python manage.py runserver 8000
```

## 📚 API Endpoints

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create employee
- `GET /api/employees/{id}/` - Get employee detail
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/stats/` - Dashboard statistics
- `GET /api/employees/count/` - Total count

### Worksites
- `GET /api/worksites/` - List all worksites
- `POST /api/worksites/` - Create worksite
- `GET /api/worksites/{id}/` - Get worksite detail
- `PUT /api/worksites/{id}/` - Update worksite
- `DELETE /api/worksites/{id}/` - Delete worksite

## 🔧 Project Structure

```
portalsync-backend/
├── config/           # Project settings
├── employees/        # Employee app
├── worksites/        # Worksite app
├── benefits/         # Benefits queue app
├── manage.py
└── requirements.txt
```

## 👨‍💻 Development

Built as part of a 4-month internship project (January - May 2026) focused on HR automation in Thailand.

## 📝 License

Private - Internal company use only