# 🔧 Troubleshooting Sign Translation System

## Issue: Signs Not Being Translated

### Quick Diagnosis Checklist

1. **Are you using the NEW translation system?**
   - ❌ OLD: Camera icon (📹) → Simple gestures only
   - ✅ NEW: 🤟 icon → Full translation system
   
2. **Is the server running?**
   ```bash
   python manage.py runserver
   ```

3. **Are static files loaded?**
   - Open browser console (F12)
   - Check for JavaScript errors

4. **Is the translation panel opening?**
   - Should see full-screen overlay with camera feed

---

## 🚀 Step-by-Step Fix

### Step 1: Restart Server with Static Files

```bash
# Stop current server (Ctrl+C)

# Collect static files
python manage.py collectstatic --noinput

# Restart server
python manage.py runserver
```

### Step 2: Clear Browser Cache

1. Open browser
2. Press `Ctrl + Shift + Delete`
3. Clear cached images and files
4. Reload page (`Ctrl + F5`)

### Step 3: Open Translation Panel

1. Go to: http://127.0.0.1:8000/
2. Look for **🤟 icon** in header (NOT the 📹 camera icon)
3. Click the 🤟 icon
4. Allow camera access
5. Full-screen translation panel should appear

### Step 4: Check Browser Console

1. Press `F12` to open Developer Tools
2. Go to "Console" tab
3. Look for errors

**Expected messages**:
```
✅ Sign Language Translator initialized
✅ SignLanguageAvatar initialized
✅ Sign Translator ready
```

**Error messages** (if any):
```
❌ TypeError: Cannot read property...
❌ Failed to load resource...
❌ Uncaught ReferenceError...
```

---

## 🎯 Test the API Directly

### Test 1: Check System Status

Open browser console and run:

```javascript
fetch('/api/translate/status/')
  .then(r => r.json())
  .then(d => console.log('System Status:', d))
  .catch(e => console.error('Error:', e));
```

**Expected Response**:
```json
{
  "status": "operational",
  "components": {
    "sign_recognizer": "ready",
    "intent_recognizer": "ready",
    "text_to_sign": "ready"
  }
}
```

### Test 2: Test Text-to-Sign

```javascript
fetch('/api/translate/text-to-sign/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: "صباح الخير"})
})
.then(r => r.json())
.then(d => console.log('Translation:', d))
.catch(e => console.error('Error:', e));
```

---

## 🐛 Common Issues & Solutions

### Issue 1: 🤟 Icon Not Visible

**Cause**: Static files not loaded

**Solution**:
```bash
# In terminal
python manage.py collectstatic --noinput
python manage.py runserver

# In browser
Ctrl + F5 (hard refresh)
```

### Issue 2: Translation Panel Not Opening

**Cause**: JavaScript not loaded

**Check**:
1. View page source (Ctrl+U)
2. Look for these lines:
   ```html
   <script src="/static/js/sign-avatar.js"></script>
   <script src="/static/js/sign-translator.js"></script>
   ```
3. Click the links - should show JavaScript code

**Solution**:
```bash
# Verify files exist
dir lowaah_app\static\js\sign-*.js

# Should show:
# sign-avatar.js
# sign-translator.js
```

### Issue 3: Camera Works But No Recognition

**Cause**: Translation controller not initializing

**Check Browser Console**:
```javascript
// Type this in console:
signTranslator

// Should show object with properties, not "undefined"
```

**Solution**:
Check for Python errors in terminal:
```bash
# Look for errors like:
[INIT ERROR] Failed to initialize translation controller...
```

### Issue 4: API Returns 404

**Cause**: URLs not registered

**Verify**:
```bash
# In terminal
python manage.py show_urls | grep translate

# Should show:
# /api/translate/sign-to-text/
# /api/translate/text-to-sign/
# /api/translate/process-request/
# /api/translate/clear-session/
# /api/translate/status/
```

---

## ✅ Verification Checklist

Run through this checklist:

- [ ] Server is running without errors
- [ ] Browser loaded without JavaScript errors  
- [ ] 🤟 icon is visible in header
- [ ] Clicking 🤟 opens full-screen panel
- [ ] Camera feed is visible
- [ ] Moving hand shows hand tracking
- [ ] API status endpoint returns "operational"
- [ ] Console shows "Sign Translator ready"

---

## 🎬 Quick Demo Test

### Manual Test Without Signs

1. Open browser console (F12)
2. Type:
   ```javascript
   signTranslator.translateTextToSign("صباح الخير");
   ```
3. Avatar should animate showing "Good Morning" in signs

If this works → System is working, issue is with sign recognition
If this fails → System initialization problem

---

## 📞 Still Not Working?

### Get Detailed Error Info

```javascript
// In browser console
console.log('Translation Controller:', signTranslator);
console.log('Avatar:', signTranslator?.avatar);
console.log('Video Element:', document.getElementById('sign-video'));
console.log('Camera Active:', signTranslator?.isTranslating);

// Test API manually
fetch('/api/translate/status/')
  .then(r => r.text())
  .then(text => console.log('Raw Response:', text));
```

### Check Python Backend

```bash
# In terminal where server is running
# Look for these initialization messages:

[INIT] Initializing translation controller...
✅ SignSequenceRecognizer initialized (LSTM: False)
✅ IntentRecognizer initialized with Absher services
✅ TextToSignTranslator initialized
✅ Translation Controller ready!
[INIT] Translation controller initialized successfully!
```

---

## 🔄 Complete Reset Procedure

If nothing works, do a complete reset:

```bash
# 1. Stop server (Ctrl+C)

# 2. Clear Python cache
python -c "import shutil, os; [shutil.rmtree(os.path.join(root, d)) for root, dirs, _ in os.walk('.') for d in dirs if d == '__pycache__']"

# 3. Clear static files
rmdir /s staticfiles  # Windows
# rm -rf staticfiles  # Linux/Mac

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Restart server
python manage.py runserver

# 6. In browser:
# - Clear cache (Ctrl+Shift+Delete)
# - Hard refresh (Ctrl+F5)
# - Try again
```

---

## 📸 What You Should See

### Correct Setup:

1. **Header**: 🤟 icon visible (NOT just 📹)
2. **Click 🤟**: Full-screen black overlay appears
3. **Panel**: Shows camera feed + text area + controls
4. **Moving hand**: Hand skeleton visible on video
5. **Making signs**: Text appears in recognition area
6. **Confidence**: Shows percentage (e.g., 85%)

### Old System (NOT what we want):

1. Click 📹 camera icon
2. Side panel appears (not full screen)
3. Simple gesture detection only
4. No translation, just navigation

---

## 🎯 Expected Behavior

When working correctly:

1. **Start signing** → See your hand tracked
2. **Hold sign for 2 seconds** → Current sign appears with confidence
3. **Complete word** → Word added to text area
4. **Multiple signs** → Sentence builds up
5. **Click "Execute"** → Intent recognized, avatar responds
6. **Avatar animates** → Shows response in sign language
7. **Auto-navigate** → Goes to correct service page

---

## 🆘 Emergency: Use Old System

If translation system won't work, you can still use the old gesture system:

1. Click **📹 icon** (camera, not 🤟)
2. Use these simple gestures:
   - Open hand → Services
   - Rock sign (🤘) → Violations  
   - Thumbs up → Confirm
   - Thumbs down → Back

The old system works but has limited features.

---

**Need more help? Check browser console for specific error messages and share them.**


