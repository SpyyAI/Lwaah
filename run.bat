@echo off
REM Lowaah Quick Launch Script for Windows

echo ================================================
echo         LOWAAH - Saudi Sign Language Assistant
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo [INFO] Checking dependencies...
pip show django >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

REM Check if model exists
if not exist "lowaah_app\ai\gesture_model.pkl" (
    echo [INFO] Training AI model...
    python lowaah_app\ai\train_model.py
)

REM Run migrations
echo [INFO] Running migrations...
python manage.py migrate --noinput

REM Start server
echo.
echo ================================================
echo [SUCCESS] Starting Django development server...
echo ================================================
echo.
echo Visit: http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

pause

