# 🚀 Quick Start Guide - لواح Lowaah

## Installation (5 minutes)

### Option 1: Automatic Setup (Recommended)

```bash
# Windows
python setup.py

# Linux/Mac
python3 setup.py
```

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Train AI model
python lowaah_app/ai/train_model.py

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Run server
python manage.py runserver
```

## 🎯 First Steps

1. **Open Browser**: Navigate to http://127.0.0.1:8000/

2. **Enable Camera**: Click the 📹 camera icon in the header

3. **Allow Access**: Grant webcam permissions when prompted

4. **Try Gestures**: 
   - Show open palm → Navigate to Services
   - Make a fist → Go to Violations
   - Thumbs up → Approve/Next

## 🤟 Gesture Cheat Sheet

| Gesture | Action |
|---------|--------|
| ✋ Open Hand | Services |
| ✊ Closed Fist | Violations |
| 👍 Thumbs Up | Approve |
| 👎 Thumbs Down | Back |
| ☝️ Index Point | Select |
| ✌️ Victory | Absher Individuals |

## ⌨️ Keyboard Shortcuts

- `Alt + C` - Toggle camera
- `Alt + H` - Home
- `Alt + S` - Services
- `Alt + V` - Violations
- `Escape` - Close camera

## 🔧 Troubleshooting

### Camera Not Working?

1. Check browser permissions (Settings → Privacy)
2. Ensure no other app is using the camera
3. Try a different browser (Chrome recommended)

### Model Not Loading?

```bash
# Retrain the model
python lowaah_app/ai/train_model.py
```

### Static Files Not Loading?

```bash
# Recollect static files
python manage.py collectstatic --noinput
```

## 📚 Next Steps

- Read the [full README](README.md)
- Customize gestures in `lowaah_app/ai/train_model.py`
- Add more services in `lowaah_app/views.py`
- Improve UI in `lowaah_app/static/css/style.css`

## 💬 Need Help?

- Check [API Documentation](README.md#api-documentation)
- Review [Project Structure](README.md#project-structure)
- Open an issue on GitHub

---

**Ready to contribute?** See [CONTRIBUTING](README.md#contributing)

صنع بـ ❤️ للمجتمع السعودي

