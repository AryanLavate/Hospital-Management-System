# Hospital Management System

A web-based hospital management application built with Django and MySQL to manage patients, doctors, appointments, and administrative workflows.

## Features

- Role-based hospital workflow support
- Patient and doctor management
- Appointment scheduling and tracking
- Dashboard and reporting views
- Static/media file handling for Django apps

## Tech Stack

- Python
- Django
- MySQL
- HTML/CSS/JavaScript

## Project Structure

- `hospital_system/` - Django project configuration
- `core/` - main app logic, models, views, templates integration
- `templates/` - shared HTML templates
- `static/` - static assets (CSS, JS, images)
- `manage.py` - Django management entry point

## Getting Started

### Prerequisites

- Python 3.10 or newer
- MySQL Server
- `pip`

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Use template files for local configuration:

- `db_config.example.py` -> `db_config.py`
- `.env.example` -> `.env`

Set appropriate database and Django environment values before running.

### Database Setup

```bash
python setup_db.py
python init_database.py
```

### Run the Application

```bash
python manage.py runserver
```

Windows helper:

```bat
run_app.bat
```

## Security

Sensitive files such as `.env` and `db_config.py` are excluded from version control via `.gitignore`. Only example/template config files should be committed.

## License

This project is provided for educational and development use.
