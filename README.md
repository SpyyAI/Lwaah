# لواح - Lowaah | Saudi Sign Language Assistant

<div align="center">

![Lowaah Logo](https://via.placeholder.com/150x150?text=🤟)

**A Django-based web application that enables deaf and hard-of-hearing users to navigate government services using Saudi Sign Language (KSL)**

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [العربية](#arabic)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Gestures](#supported-gestures)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**Lowaah** (لواح) is an innovative accessibility platform that bridges the gap between deaf/hard-of-hearing individuals and government services. Built with Django and powered by AI, it provides a seamless interface where users can communicate using **Saudi Sign Language (KSL)** - translating signs to text, understanding intent, and responding back in sign language via a 3D avatar.

### 🆕 Version 2.0 - Full Sign Language Translation System

This system goes beyond simple gesture commands - it provides **complete bi-directional translation**:
- ✅ **Sign → Text**: Real-time recognition of 200+ KSL signs
- ✅ **Text → Intent**: NLP understanding of user requests
- ✅ **Intent → Action**: Automatic service routing and execution
- ✅ **Response → Signs**: 3D avatar displaying responses in sign language

### Key Technologies

- **Backend**: Django 5+ with Django REST Framework
- **AI/ML**: 
  - MediaPipe for hand tracking
  - LSTM (TensorFlow/Keras) for sequence recognition
  - NLP for intent recognition
- **Frontend**: 
  - HTML5, CSS3, JavaScript (Vanilla)
  - Three.js for 3D avatar rendering
- **Computer Vision**: OpenCV for image processing
- **Design**: Absher-inspired UI with Arabic/English bilingual support

---

## ✨ Features

### 🤟 Full Sign Language Translation (NEW!)
- **Bi-directional translation**: Sign ↔ Text ↔ Sign
- **200+ vocabulary**: Letters, words, phrases, service keywords
- **Real-time recognition**: LSTM-based sequence analysis at 10 FPS
- **3D avatar output**: Three.js powered sign language responses
- **Intent understanding**: NLP recognizes what users want
- **11+ service intents**: Violations, ID renewal, licenses, passports, etc.

### 🎨 Absher-Style UI
- Familiar interface matching Saudi government platforms
- Green/white color scheme (#006837)
- Fully responsive design
- Arabic/English bilingual support
- **NEW**: Translation panel with live camera feed and avatar

### 🚀 Smart Navigation
- **NEW**: Intent-based automatic routing
- **NEW**: Suggested actions based on user request
- Visual feedback for detected gestures
- Confidence indicators
- Auto-execution of service actions

### ♿ Accessibility
- Designed for deaf and hard-of-hearing users
- **NEW**: Complete sign language communication
- **NEW**: Visual avatar responses
- Keyboard shortcuts support
- Screen reader compatible
- High contrast modes

### 🔒 Security
- No server-side image storage
- POST-only API endpoints
- CSRF protection
- Secure session management

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Webcam     │  │   Canvas     │  │  UI Display  │     │
│  │   Capture    │→│  Processing  │→│   & Feedback │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│           ↓                                    ↑             │
│       Base64 Frame                       JSON Response      │
│           ↓                                    ↑             │
└───────────┼────────────────────────────────────┼────────────┘
            ↓                                    ↑
    ┌───────────────────────────────────────────────────┐
    │                REST API Layer                      │
    │         POST /api/detect-gesture/                  │
    └───────────────────────────────────────────────────┘
            ↓                                    ↑
    ┌───────────────────────────────────────────────────┐
    │              Django Backend                        │
    │  ┌─────────────┐  ┌──────────────┐               │
    │  │ Hand        │  │  Gesture     │               │
    │  │ Detector    │→│  Classifier  │               │
    │  └─────────────┘  └──────────────┘               │
    │         ↓                ↑                         │
    │  MediaPipe      Scikit-Learn Model                │
    └───────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Webcam (for gesture detection)
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/lowaah.git
cd lowaah
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the AI Model

```bash
python lowaah_app/ai/train_model.py
```

This will generate `gesture_model.pkl` with synthetic training data. For production, replace with real gesture data.

### Step 5: Run Migrations

```bash
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📱 Usage

### Starting the Application

1. Open your browser and navigate to `http://127.0.0.1:8000/`
2. Click the camera icon (📹) in the header
3. Allow webcam access when prompted
4. The gesture detection panel will appear

### Using Gestures

1. Position your hand in front of the webcam
2. Perform one of the supported gestures
3. Wait for the system to detect and display the gesture
4. The system will automatically navigate based on the gesture

### Keyboard Shortcuts

- `Alt + C`: Toggle camera panel
- `Alt + H`: Go to home
- `Alt + S`: Go to services
- `Alt + V`: Go to violations
- `Escape`: Close camera panel

---

## 🤟 Supported Gestures

| Gesture | Action | Arabic | URL |
|---------|--------|--------|-----|
| Open Hand | Navigate to Services | يد مفتوحة → الخدمات | `/services/` |
| Closed Fist | Go to Violations | قبضة مغلقة → المخالفات | `/violations/` |
| Thumbs Up | Approve/Next | إبهام لأعلى → موافق | Action |
| Thumbs Down | Reject/Back | إبهام لأسفل → رجوع | Action |
| Pointing Index | Select Item | إشارة السبابة → تحديد | Action |
| Victory Sign | Absher Individuals | علامة V → أبشر أفراد | `/absher-individuals/` |
| Palm Right | Navigate Right | يمين | Action |
| Palm Left | Navigate Left | يسار | Action |

---

## 🔌 API Documentation

### Detect Gesture

**Endpoint**: `POST /api/detect-gesture/`

**Request**:
```json
{
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response**:
```json
{
  "gesture": "thumbs_up",
  "confidence": 0.95,
  "success": true
}
```

**Error Response**:
```json
{
  "error": "No frame provided",
  "success": false
}
```

### Gesture Information

**Endpoint**: `GET /api/gesture-info/`

**Response**:
```json
{
  "gestures": [
    {
      "label": "open_hand",
      "action": "Navigate to My Services",
      "description": "Show an open palm with all fingers spread",
      "url": "/services/"
    }
  ],
  "total": 8
}
```

### Health Check

**Endpoint**: `GET /api/health/`

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "Lowaah Sign Language Assistant is running"
}
```

---

## 📁 Project Structure

```
lowaah/
├── core/                      # Django project configuration
│   ├── settings.py           # Main settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
│
├── lowaah_app/               # Main application
│   ├── ai/                   # AI/ML module
│   │   ├── train_model.py    # Model training script
│   │   ├── hand_detector.py  # Gesture detection
│   │   ├── gesture_model.pkl # Trained model
│   │   └── gesture_labels.pkl # Label mapping
│   │
│   ├── static/               # Static files
│   │   ├── css/
│   │   │   └── style.css     # Absher-style CSS
│   │   └── js/
│   │       ├── camera.js     # Webcam & detection
│   │       └── navigation.js # Navigation logic
│   │
│   ├── templates/            # HTML templates
│   │   └── lowaah_app/
│   │       ├── base.html     # Base template
│   │       ├── index.html    # Dashboard
│   │       ├── services.html # Services page
│   │       ├── violations.html
│   │       ├── id_renewal.html
│   │       ├── absher_individuals.html
│   │       ├── success.html
│   │       └── login.html
│   │
│   ├── views.py              # Django views
│   ├── urls.py               # App URLs
│   └── models.py             # Database models
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🛠️ Development

### Testing Gesture Detection

Test the detector standalone:

```bash
python lowaah_app/ai/hand_detector.py
```

This opens a webcam window showing real-time gesture detection.

### Training with Real Data

1. Collect gesture images in folders:
   ```
   dataset/
   ├── open_hand/
   ├── closed_fist/
   ├── thumbs_up/
   └── ...
   ```

2. Modify `train_model.py` to load your dataset

3. Retrain:
   ```bash
   python lowaah_app/ai/train_model.py
   ```

### Running Tests

```bash
python manage.py test
```

### Code Style

```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .
isort .

# Check style
flake8 .
```

---

## 🌐 Deployment

### Production Settings

1. Update `core/settings.py`:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = 'your-secure-secret-key'
   ```

2. Use environment variables for sensitive data

### Deploy with Gunicorn

```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Deploy with Nginx

Create nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/lowaah/staticfiles/;
    }
}
```

### Docker Deployment

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution

- [ ] Improve gesture recognition accuracy
- [ ] Add more Saudi Sign Language gestures
- [ ] Enhance UI/UX
- [ ] Add multilingual support (beyond Arabic/English)
- [ ] Improve documentation
- [ ] Write tests
- [ ] Optimize performance

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe**: For excellent hand tracking
- **Absher Platform**: UI/UX inspiration
- **Saudi Sign Language Community**: For gesture references
- **Django Community**: For the amazing framework

---

## 📞 Contact

**Project Maintainer**: Your Name

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Basic gesture recognition (8 gestures)
- ✅ Absher-style UI
- ✅ Core navigation features

### Phase 2 (Next)
- [ ] Real-world gesture dataset collection
- [ ] Improved model accuracy (>95%)
- [ ] User accounts and profiles
- [ ] Gesture customization

### Phase 3 (Future)
- [ ] Mobile app (React Native)
- [ ] Integration with actual government APIs
- [ ] Advanced analytics dashboard
- [ ] AI-powered assistance

---

<div align="center">

**Made with ❤️ for the Saudi deaf and hard-of-hearing community**

صُنع بـ ❤️ للمجتمع السعودي من الصم وضعاف السمع

</div>

