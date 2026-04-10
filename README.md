# Hospital Management System

A Django-based hospital management project with MySQL support.

## Requirements

- Python 3.10+
- MySQL Server
- Pip

## 1) Install dependencies

```bash
pip install -r requirements.txt
```

## 2) Configure database credentials (local only)

1. Copy `db_config.example.py` to `db_config.py`
2. Update values in `db_config.py`:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASS`
   - `DB_PORT`
   - `DB_NAME`

Do not commit `db_config.py` or any `.env` files. They are ignored by `.gitignore`.
You can use `.env.example` as a template for local environment variables.

## 3) Initialize database

```bash
python setup_db.py
python init_database.py
```

## 4) Run the application

```bash
python manage.py runserver
```

Or run the helper script on Windows:

```bat
run_app.bat
```

## GitHub push (safe steps)

```bash
git init
git add .
git status
git commit -m "Initial commit: hospital management system"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

If a secret file is accidentally staged, unstage it:

```bash
git restore --staged db_config.py
git restore --staged .env
```

If you accidentally add an unwanted folder, remove it from Git tracking:

```bash
git rm -r --cached travel_tourism_booking_system
```

## Notes

- Keep secrets only in local files (`db_config.py`, `.env`).
- Use `db_config.example.py` as the shared template for collaborators.
