# Install Tesseract OCR for Real Card Scanning

## 🎯 What We Need

To read text from your actual cards, you need to install **Tesseract OCR** - the software that reads text from images.

---

## 📥 **STEP 1: Download Tesseract**

### Windows Installation:

**Click this link to download:**
👉 **https://github.com/UB-Mannheim/tesseract/wiki**

Or direct download:
👉 **https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe**

**File**: `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (~80 MB)

---

## 📦 **STEP 2: Install Tesseract**

1. **Run the downloaded `.exe` file**

2. **IMPORTANT: During installation:**
   - ✅ Check "Additional language data"
   - ✅ Select **"Arabic"** language pack
   - ✅ Select **"English"** language pack
   - ✅ Remember installation path (usually: `C:\Program Files\Tesseract-OCR\`)

3. **Click "Install"** and wait

---

## ⚙️ **STEP 3: Add to System Path**

### Option A: Automatic (Recommended)

Run this in PowerShell (as Administrator):

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Tesseract-OCR", "Machine")
```

### Option B: Manual

1. Press `Win + X` → Select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find "Path"
5. Click "Edit" → "New"
6. Add: `C:\Program Files\Tesseract-OCR`
7. Click "OK" on all windows
8. **Restart your terminal/IDE**

---

## 🧪 **STEP 4: Test Installation**

Open a **NEW** terminal and run:

```bash
tesseract --version
```

You should see:
```
tesseract v5.3.3
```

---

## 🔧 **STEP 5: Configure Python**

If Tesseract is installed in a different location, update your code:

In `views.py`, add this line before using pytesseract:

```python
# Only if installed in non-standard location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## ✅ **STEP 6: Restart Server**

After installing Tesseract:

```bash
# Stop current server (Ctrl+C if running)

# Start server again
.\venv\Scripts\python.exe manage.py runserver
```

---

## 🧪 **STEP 7: Test Card Scanning**

1. Go to: `http://127.0.0.1:8000/profile/setup/`
2. Click "مسح البطاقة - Scan ID/License"
3. Point camera at your ID card or license
4. Click "التقاط - Capture"
5. Should now extract **REAL** text from your card! ✨

---

## 🔍 **Troubleshooting**

### Error: "Tesseract not installed"

**Solution**: Make sure you:
1. Installed Tesseract (Step 2)
2. Added to system PATH (Step 3)
3. Restarted terminal/server (Step 6)

### Error: "pytesseract not found"

**Solution**: Install Python package:
```bash
.\venv\Scripts\pip install pytesseract pillow
```

### OCR Returns Empty Text

**Solutions**:
- Use better lighting when scanning
- Hold card steady and flat
- Make sure card fills most of camera frame
- Card text should be clear and readable
- Try landscape orientation for ID cards

### Arabic Text Not Detected

**Solution**: Make sure you installed Arabic language pack during Tesseract setup (Step 2)

---

## 📊 **What Will Work After Installation**

| Card Type | What Gets Extracted |
|-----------|---------------------|
| **National ID** | Name (Arabic), 10-digit ID number |
| **Driver's License** | Name, ID number, license number |
| **Car Registration** | Plate letters (Arabic), Plate numbers |
| **Iqama** | Name, Iqama number |

---

## 💡 **Tips for Best Results**

### When Scanning:
1. **Good Lighting** - Bright, even light (no shadows)
2. **Steady Hand** - Hold still when capturing
3. **Clear View** - Card should fill 70-80% of frame
4. **Flat Card** - No wrinkles or folds
5. **Clean Card** - Wipe off dust/fingerprints
6. **Focus** - Wait for camera to focus before capturing

### Card Position:
```
❌ Too far:  [card...]
❌ Too close: [CA...]
❌ Tilted:    [/card/]
✅ Perfect:   [CARD]
```

---

## 🎯 **Expected Accuracy**

| Condition | Accuracy |
|-----------|----------|
| Perfect (good light, clear card) | 85-95% |
| Good (normal conditions) | 70-85% |
| Poor (bad light, worn card) | 40-70% |

---

## 🚀 **After Installation**

The scanner will:
- ✅ Read actual text from your cards
- ✅ Extract Arabic names
- ✅ Find ID numbers (10 digits)
- ✅ Detect plate letters and numbers
- ✅ Auto-fill form with real data

---

## 📝 **Quick Start Checklist**

- [ ] Download Tesseract (Step 1)
- [ ] Install with Arabic language pack (Step 2)
- [ ] Add to system PATH (Step 3)
- [ ] Test with `tesseract --version` (Step 4)
- [ ] Restart Django server (Step 6)
- [ ] Test card scanning (Step 7)

---

## 🎉 **Ready!**

Once installed, your scanner will actually READ your real cards!

**Installation Time**: ~5-10 minutes  
**Worth It**: Absolutely! 🚀

---

## 📞 **Need Help?**

If you get stuck:
1. Check the error message in browser console (F12)
2. Check Django server logs
3. Verify Tesseract installed: `tesseract --version`
4. Make sure you restarted the server

---

**Let me know when Tesseract is installed and I'll help you test it!** 🎯



