# 🚀 Quick Start Guide - Sign Language Translation System

## Get Started in 5 Minutes!

### Step 1: Install Dependencies (2 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/lowaah.git
cd lowaah

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Setup Database (30 seconds)

```bash
python manage.py migrate
```

### Step 3: Run Server (10 seconds)

```bash
python manage.py runserver
```

### Step 4: Open Browser & Test! (2 minutes)

1. Open: http://127.0.0.1:8000/
2. Click the **🤟** icon in the header
3. Allow camera access
4. Start signing!

---

## 🎯 Quick Test Guide

### Test Sign-to-Text Translation

1. **Open translation panel** (click 🤟 icon)
2. **Position your hand** in front of camera
3. **Perform signs** from vocabulary:
   - Open hand → Services
   - Rock sign (🤘) → Violations
   - Thumbs up → Confirm
4. **Watch text appear** in real-time
5. **Click "Execute"** to process request

### Test Text-to-Sign Translation

Use browser console:

```javascript
// Translate Arabic text to sign language
signTranslator.translateTextToSign("استعلام عن المخالفات");

// Watch the 3D avatar perform the signs!
```

---

## 📖 Available Signs

### Basic Signs (Always Work)
- ✅ **Open Hand** (يد مفتوحة) → Navigate to Services
- ✅ **Rock Sign** (🤘) → Violations Inquiry
- ✅ **Thumbs Up** (👍) → Confirm/Next
- ✅ **Thumbs Down** (👎) → Back/Cancel
- ✅ **Victory Sign** (✌️) → Absher Individuals

### Service Keywords (Arabic)
- `استعلام` (inquiry)
- `مخالفات` (violations)
- `تجديد` (renewal)
- `هوية` (ID)
- `رخصة` (license)
- `جواز` (passport)

### Action Verbs
- `أريد` (I want)
- `افتح` (open)
- `ابحث` (search)
- `عرض` (show)

### Common Phrases
Try saying (in signs):
- "استعلام عن المخالفات" → Violations Inquiry
- "تجديد الهوية" → ID Renewal
- "أريد الاستعلام" → I want to inquire

---

## 🎬 Usage Examples

### Example 1: Check Traffic Violations

**What to do**:
1. Sign: "استعلام" (inquiry) → 🔍 pointing gesture
2. Sign: "مخالفات" (violations) → ⚠️ warning gesture
3. Click "Execute" button

**System will**:
- ✅ Recognize text: "استعلام مخالفات"
- ✅ Understand intent: violations_inquiry
- ✅ Navigate to: /violations/
- ✅ Show response in sign language

### Example 2: Renew National ID

**What to do**:
1. Sign: "تجديد" (renewal)
2. Sign: "هوية" (ID)
3. Click "Execute"

**System will**:
- ✅ Recognize text: "تجديد هوية"
- ✅ Understand intent: id_renewal
- ✅ Navigate to: /id-renewal/
- ✅ Display available actions

---

## 🔧 Troubleshooting

### Camera Not Working?

**Check**:
1. Browser permissions (allow camera)
2. Camera is not in use by another app
3. Use HTTPS (required for camera on some browsers)

**Solution**:
```javascript
// Check camera status in console
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => console.log('✅ Camera works!'))
  .catch(err => console.error('❌ Camera error:', err));
```

### Signs Not Recognized?

**Tips**:
1. **Lighting**: Ensure good lighting (face a window)
2. **Background**: Use plain background
3. **Distance**: Keep hand 30-50cm from camera
4. **Speed**: Sign slowly and clearly
5. **Stability**: Hold sign for 1-2 seconds

### Low Confidence?

**Improve accuracy**:
- Practice signs from gesture guide
- Ensure hand is clearly visible
- Avoid overlapping fingers
- Keep hand in center of frame

---

## 📚 Next Steps

### Learn More Signs
- Visit: http://127.0.0.1:8000/gesture-help/
- Watch tutorial videos
- Practice with vocabulary list

### Customize Vocabulary
Edit: `lowaah_app/ai/sign_language_vocabulary.py`

```python
# Add your custom sign
CUSTOM_SIGNS = {
    'my_sign': {
        'english': 'my sign',
        'category': 'custom',
        'intent': 'my_action'
    }
}
```

### Train Custom Model
See: `SIGN_LANGUAGE_TRANSLATION_SYSTEM.md` → Training Section

---

## 🎉 Success Indicators

You know it's working when:
- ✅ Camera panel opens smoothly
- ✅ Video feed shows your hand
- ✅ Text appears as you sign
- ✅ Confidence bar shows > 60%
- ✅ Intent is recognized correctly
- ✅ Avatar displays response signs

---

## 🆘 Need Help?

**Documentation**:
- Full System: `SIGN_LANGUAGE_TRANSLATION_SYSTEM.md`
- Main README: `README.md`

**Support**:
- GitHub Issues: Report bugs
- Email: support@lowaah.sa

---

## 🌟 Pro Tips

1. **Practice common phrases** first
2. **Use good lighting** always
3. **Sign at normal speed** (not too fast)
4. **Clear hand gestures** (avoid blur)
5. **Use two hands** for complex signs
6. **Check confidence** before executing
7. **Restart session** if stuck (click Clear button)

---

**Happy Signing! 🤟**

Made with ❤️ for accessibility


