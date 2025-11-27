#!/bin/bash
# Lowaah Quick Launch Script for Linux/Mac

echo "================================================"
echo "         LOWAAH - Saudi Sign Language Assistant"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[INFO] Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "[INFO] Checking dependencies..."
if ! python -c "import django" 2>/dev/null; then
    echo "[INFO] Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if model exists
if [ ! -f "lowaah_app/ai/gesture_model.pkl" ]; then
    echo "[INFO] Training AI model..."
    python lowaah_app/ai/train_model.py
fi

# Run migrations
echo "[INFO] Running migrations..."
python manage.py migrate --noinput

# Start server
echo ""
echo "================================================"
echo "[SUCCESS] Starting Django development server..."
echo "================================================"
echo ""
echo "Visit: http://127.0.0.1:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver

