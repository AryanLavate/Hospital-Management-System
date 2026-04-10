import os
import sys
import django
import MySQLdb
from datetime import date, time, timedelta

# Load database config from db_config.py
try:
    import db_config
    db_host = db_config.DB_HOST
    db_user = db_config.DB_USER
    db_pass = db_config.DB_PASS
    db_port = getattr(db_config, 'DB_PORT', '3306')
    db_name = getattr(db_config, 'DB_NAME', 'smart_hospital_db')
except ImportError:
    print("\n[ERROR] db_config.py not found!")
    print("Copy db_config.example.py to db_config.py and edit with your database credentials.")
    print("  Windows: copy db_config.example.py db_config.py")
    print("  Then edit db_config.py with your MySQL host, user, and password.\n")
    sys.exit(1)

# 1. Create Database
print(f"Step 1: Connecting to MySQL at {db_host} as {db_user}...")
try:
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, port=int(db_port))
    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    db.close()
    print(f"Database '{db_name}' verified/created.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    print("\n[TIP] Make sure MySQL is running and your credentials in db_config.py are correct.")
    exit(1)

# 2. Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import Patient, Doctor, Appointment, Bill

# 3. Run Migrations
print("Step 2: Running migrations...")
try:
    call_command('makemigrations', 'core')
    call_command('migrate')
    print("Migrations applied successfully.")
except Exception as e:
    print(f"Error running migrations: {e}")
    exit(1)

# 4. Seed Data
print("Step 3: Seeding sample data...")
try:
    #   Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created (PW: admin123).")
    
    #   Doctors
    d1_user, _ = User.objects.get_or_create(username='dr_smith', defaults={'first_name': 'John', 'last_name': 'Smith'})
    d1_user.set_password('dr123')
    d1_user.save()
    
    d2_user, _ = User.objects.get_or_create(username='dr_jones', defaults={'first_name': 'Sarah', 'last_name': 'Jones'})
    d2_user.set_password('dr123')
    d2_user.save()

    d1, _ = Doctor.objects.get_or_create(user=d1_user, defaults={
        'specialization': 'Cardiology',
        'phone': '1234567890',
        'email': 'smith@hospital.com',
        'schedule': 'Mon-Wed-Fri: 9:00 AM - 2:00 PM'
    })
    
    d2, _ = Doctor.objects.get_or_create(user=d2_user, defaults={
        'specialization': 'Pediatrics',
        'phone': '0987654321',
        'email': 'jones@hospital.com',
        'schedule': 'Tue-Thu: 10:00 AM - 4:00 PM'
    })

    #   Patients
    p1, _ = Patient.objects.get_or_create(name='Alice Wonderland', defaults={
        'age': 28, 'gender': 'F', 'phone': '555-0199', 'address': '123 Rabbit Hole Lane', 'medical_history': 'Asthma'
    })
    
    p2, _ = Patient.objects.get_or_create(name='Bob Builder', defaults={
        'age': 45, 'gender': 'M', 'phone': '555-2020', 'address': 'Construction Way #4', 'medical_history': 'No allergies'
    })

    #   Appointments
    today = date.today()
    Appointment.objects.get_or_create(patient=p1, doctor=d1, date=today + timedelta(days=1), time=time(10, 0), defaults={'status': 'Scheduled'})
    a2, _ = Appointment.objects.get_or_create(patient=p2, doctor=d2, date=today, time=time(14, 0), defaults={'status': 'Completed'})

    #   Bill
    if not Bill.objects.filter(patient=p2, appointment=a2).exists():
        Bill.objects.create(patient=p2, appointment=a2, consultation_fee=500.00, medicine_charges=150.00, other_charges=20.00, payment_status='Paid')

    print("Sample data seeded successfully.")
except Exception as e:
    print(f"Error seeding data: {e}")

print("\nSetup Complete! You can now run the project using 'run_app.bat'.")
