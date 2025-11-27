# 🎯 How to Use the Sign Language Translation System

## ✅ Backend Status: WORKING!

Your system is fully functional. Follow these steps carefully:

---

## 🚀 Step-by-Step Instructions

### Step 1: Start the Server

```bash
# In PowerShell/Command Prompt
venv\Scripts\python.exe manage.py runserver
```

**Wait for**:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Step 2: Open Browser

1. Open Chrome, Firefox, or Edge
2. Go to: **http://127.0.0.1:8000/**
3. You should see the Lowaah homepage

---

### Step 3: Find the RIGHT Button

**⚠️ IMPORTANT: There are TWO different systems!**

| Icon | System | What it does |
|------|--------|--------------|
| 📹 **Camera icon** | OLD Gesture System | Simple gestures only (open hand, thumbs up, etc.) |
| 🤟 **Hand icon** | NEW Translation System | Full sign language translation! |

**You MUST click the 🤟 icon** (not the camera icon!)

---

### Step 4: Open Translation Panel

1. Look at the **TOP RIGHT** of the page
2. Find the **🤟 hand icon**
3. Click it

**What should happen**:
- Full-screen black overlay appears
- Translation panel opens
- Camera feed visible
- Text area for recognized signs

**If you don't see 🤟 icon**:
```bash
# Clear browser cache:
# Chrome: Ctrl + Shift + Delete
# Then: Ctrl + F5 (hard refresh)
```

---

### Step 5: Allow Camera Access

- Browser will ask for camera permission
- Click **"Allow"**
- Your camera feed should appear

---

### Step 6: Start Signing!

**How it works**:

1. **Position your hand** in front of camera (30-50cm away)
2. **Make a sign** (hold for 2 seconds)
3. **Watch the text area** - recognized words appear
4. **Build a sentence** by signing multiple words
5. **Click "Execute"** button
6. **System responds** with avatar animation

---

## 📝 Example: Check Violations

### Signs to make:

1. **Sign "استعلام"** (inquiry):
   - Point forward with index finger
   - Hold for 2 seconds

2. **Sign "مخالفات"** (violations):
   - Make warning gesture
   - Hold for 2 seconds

### What should happen:

```
✅ Recognized text appears: "استعلام مخالفات"
✅ Intent shows: "Violations Inquiry (88%)"
✅ Click "Execute"
✅ Avatar responds in sign language
✅ System navigates to violations page
```

---

## 🐛 Troubleshooting

### Problem: "I don't see the 🤟 icon"

**Solution**:
1. Clear browser cache (Ctrl + Shift + Delete)
2. Hard refresh (Ctrl + F5)
3. Check browser console (F12) for errors

### Problem: "Panel doesn't open"

**Solution**:
1. Open browser console (F12)
2. Type: `signTranslator`
3. Should show an object (not "undefined")
4. If undefined → JavaScript not loaded

### Problem: "Camera shows but no recognition"

**Check**:
1. Is your hand visible in the camera?
2. Are you holding the sign for 2+ seconds?
3. Is there good lighting?
4. Try moving hand closer/further

### Problem: "Low confidence (<60%)"

**Improve**:
1. Better lighting
2. Plain background
3. Hold sign longer
4. Make clearer gestures
5. Keep hand in center of frame

---

## 🎮 Quick Test (No Signing Required)

Test if the system works without making signs:

1. **Open browser console** (F12)
2. **Paste this**:
   ```javascript
   signTranslator.translateTextToSign("صباح الخير");
   ```
3. **Press Enter**
4. **Avatar should animate** showing "Good Morning" in signs

**If this works** → System is perfect, just practice your signs!
**If this fails** → JavaScript issue, refresh the page

---

## 📸 What You Should See

### Correct Setup:

```
┌─────────────────────────────────────────┐
│  Lowaah Header                          │
│                           📹  🤟  👤    │ ← 🤟 icon HERE
└─────────────────────────────────────────┘

After clicking 🤟:

┌─────────────────────────────────────────────────────────┐
│ 🤟 ترجمة لغة الإشارة - Sign Language Translation    ✕ │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────┐  ┌──────────────────────────────┐ │
│  │                │  │ النص المترجم                 │ │
│  │  Camera Feed   │  │                              │ │
│  │                │  │  [Your recognized text...]   │ │
│  │     📷         │  │                              │ │
│  │                │  │  🗑️ مسح    ✅ تنفيذ         │ │
│  └────────────────┘  └──────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Success Checklist

Before reporting issues, verify:

- [ ] Server is running (`python manage.py runserver`)
- [ ] Browser opened to http://127.0.0.1:8000/
- [ ] Can see the homepage
- [ ] 🤟 icon is visible in header
- [ ] Clicked 🤟 icon (NOT 📹)
- [ ] Full-screen panel appeared
- [ ] Camera feed is visible
- [ ] Allowed camera permission
- [ ] Hand is visible in camera
- [ ] Good lighting
- [ ] Holding signs for 2+ seconds

---

## 🎯 Available Signs

### Quick Reference:

| Sign | Arabic | Meaning |
|------|--------|---------|
| Point forward | استعلام | Inquiry |
| Warning gesture | مخالفات | Violations |
| Circular motion | تجديد | Renewal |
| Card showing | هوية | ID |
| Open hand | خدمات | Services |

**For complete vocabulary**: See `sign_language_vocabulary.py`

---

## 🆘 Still Not Working?

### Get Error Details:

1. Open browser console (F12)
2. Go to "Console" tab
3. Look for red error messages
4. Share the error messages

### Common Errors:

```javascript
// Good:
✅ Sign Language Translator initialized
✅ SignLanguageAvatar initialized
✅ Sign Translator ready

// Bad:
❌ TypeError: Cannot read property...
❌ Failed to load resource...
❌ signTranslator is not defined
```

---

## 📞 Need Help?

1. Check `TEST_TRANSLATION_SYSTEM.md`
2. Run `test_translation_quick.py`
3. Check browser console for errors
4. Verify you're clicking 🤟 (not 📹)

---

**Remember**: 
- **🤟 = NEW Translation System** (what you want!)
- **📹 = OLD Gesture System** (simple gestures only)

Use the 🤟 icon for full sign language translation!


