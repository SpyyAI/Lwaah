@echo off
echo ============================================================
echo Installing Lowaah Translation System Dependencies
echo ============================================================
echo.

echo Step 1: Activating virtual environment...
call venv\Scripts\activate
echo.

echo Step 2: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 3: Installing requirements...
pip install -r requirements.txt
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Now run: python manage.py runserver
echo Then open: http://127.0.0.1:8000/
echo.
pause


