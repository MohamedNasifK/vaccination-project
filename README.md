# VacciTrack — Child Immunization Management System

A web application built with **Python**, **Django**, and **MySQL** to digitalize and streamline child immunization tracking.

---

## Features

- **Role-Based Authentication** — Admin, Doctor, and Parent/Guardian roles
- **Child Profiles** — Register and manage children with medical details
- **Vaccination Records** — Track immunization history, doses, and status
- **Appointment Scheduling** — Book, confirm, and manage vaccination appointments
- **Automated Reminders** — Send email reminders for upcoming/overdue vaccinations
- **Vaccine Directory** — Manage the full list of vaccines with recommended schedules
- **Admin Dashboard** — System-wide overview of children, appointments, and records
- **Overdue Detection** — Automatically flag missed/overdue vaccinations

---

## Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Python 3.10+, Django 4.2 |
| Database   | MySQL 8.0+          |
| Frontend   | Bootstrap 5, Font Awesome 6 |
| Fonts      | Plus Jakarta Sans, DM Sans |

---

## Project Structure

```
vaccination_project/
├── manage.py
├── requirements.txt
├── vaccination_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── vaccination_app/
    ├── models.py          # UserProfile, Child, Vaccine, VaccinationRecord, Appointment
    ├── views.py           # All views
    ├── forms.py           # Django forms
    ├── urls.py            # App URL routing
    ├── admin.py           # Admin panel registration
    ├── management/
    │   └── commands/
    │       └── seed_vaccines.py   # Seed standard vaccines
    └── templates/
        └── vaccination_app/
            ├── base.html
            ├── login.html
            ├── register.html
            ├── dashboard.html
            ├── children_list.html
            ├── child_detail.html
            ├── child_form.html
            ├── appointments_list.html
            ├── appointment_form.html
            ├── records_list.html
            ├── record_form.html
            ├── vaccines_list.html
            ├── vaccine_form.html
            ├── users_list.html
            └── confirm_delete.html
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vaccination-project.git
cd vaccination-project
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

Log into MySQL and create the database:

```sql
CREATE DATABASE vaccination_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then update `vaccination_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vaccination_db',
        'USER': 'root',              # your MySQL username
        'PASSWORD': 'your_password', # your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed Vaccines

```bash
python manage.py seed_vaccines
```

### 7. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Then manually create a `UserProfile` for the superuser via the Django admin or shell:

```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from vaccination_app.models import UserProfile
user = User.objects.get(username='your_superuser_name')
UserProfile.objects.create(user=user, role='admin')
exit()
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to: **http://127.0.0.1:8000/**

---

## User Roles

| Role            | Access                                                          |
|-----------------|-----------------------------------------------------------------|
| **Admin**       | Full system access — users, all records, appointments, reports |
| **Doctor**      | View patients, manage vaccination records, appointments        |
| **Parent**      | Manage own children, book appointments, view immunization records |

---

## Email Reminders

To enable real email reminders, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # Use Gmail App Password
```

> During development, reminders are printed to the console by default.

---

## License

MIT License — free to use and modify.
