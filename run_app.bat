@echo off
setlocal
title Healing Haven - Runner

echo ======================================================
echo   Healing Haven - Startup
echo ======================================================
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in your system PATH.
    echo Please install Python and ensure 'Add Python to PATH' is checked.
    pause
    exit /b
)

:: 2. Check if manage.py exists
if not exist "manage.py" (
    echo [ERROR] manage.py not found in the current directory.
    echo Please make sure you are running this from the project root.
    pause
    exit /b
)

:: 3. Check if db_config.py exists (required for database connection)
if not exist "db_config.py" (
    echo [ERROR] db_config.py not found!
    echo.
    echo On a new device, you need to:
    echo   1. Copy db_config.example.py to db_config.py
    echo   2. Edit db_config.py with your MySQL host, user, and password
    echo   3. Run: python setup_db.py
    echo   4. Then run this script again.
    echo.
    if exist "db_config.example.py" (
        echo Creating db_config.py from template...
        copy db_config.example.py db_config.py
        echo.
        echo db_config.py created. Please EDIT it with your database credentials, then run setup_db.py.
        pause
        exit /b
    )
    pause
    exit /b
)

:: 4. Run the server
echo Starting Django Server...
echo Visit http://127.0.0.1:8000/ when the server starts.
echo.

python manage.py runserver
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The server failed to start. 
    echo This might be due to missing dependencies or database issues.
    echo Try running: pip install django mysqlclient django-bootstrap5
    echo Then run: python setup_db.py  (after editing db_config.py)
    echo.
    pause
)

endlocal
