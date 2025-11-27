# 🚀 HOW TO START THE LOWAAH SERVER

## ⚠️ THE PROBLEM:
- Django REST Framework is not installed
- Virtual environment not activating properly
- Camera detection won't work without the server running

---

## ✅ SOLUTION - Follow These Steps:

### **Step 1: Open PowerShell as Administrator**
1. Press `Windows + X`
2. Click "Windows PowerShell (Admin)" or "Terminal (Admin)"
3. Navigate to your project:
```powershell
cd "C:\Users\Mohanad alotaibe\Desktop\Lwaah"
```

### **Step 2: Enable Script Execution (One-Time Setup)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Type `Y` and press Enter when prompted.

### **Step 3: Activate Virtual Environment**
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of your command prompt.

### **Step 4: Install Requirements**
```powershell
pip install -r requirements.txt
```

Wait for it to finish installing all packages including:
- djangorestframework
- opencv-python
- mediapipe
- scikit-learn
- pillow

### **Step 5: Run Migrations**
```powershell
python manage.py migrate
```

### **Step 6: Start Server**
```powershell
python manage.py runserver
```

### **Step 7: Open Browser**
Go to: **http://127.0.0.1:8000/**

---

## 🎯 QUICK ONE-LINE COMMAND (After Step 2):

```powershell
cd "C:\Users\Mohanad alotaibe\Desktop\Lwaah" ; .\venv\Scripts\Activate.ps1 ; python manage.py runserver
```

---

## 🔍 VERIFY IT'S WORKING:

### **Check 1: Server Running**
You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### **Check 2: Camera Button**
1. Open http://127.0.0.1:8000/
2. Click camera button (📹)
3. Camera panel should open on the left
4. Do a gesture (👍 thumbs up)
5. It should detect it!

---

## ❌ IF STILL NOT WORKING:

### **Check if packages are installed:**
```powershell
pip list | Select-String "rest_framework|opencv|mediapipe"
```

Should show:
- djangorestframework
- opencv-python  
- mediapipe

### **If missing, install manually:**
```powershell
pip install djangorestframework opencv-python mediapipe scikit-learn pillow numpy
```

---

## 📝 TROUBLESHOOTING:

### **Error: "Execution Policy"**
Run PowerShell as Administrator and:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "No module named 'rest_framework'"**
```powershell
.\venv\Scripts\Activate.ps1
pip install djangorestframework
```

### **Error: "No module named 'cv2'"**
```powershell
.\venv\Scripts\Activate.ps1
pip install opencv-python
```

---

## 🎯 ALTERNATIVE: Use CMD Instead of PowerShell

If PowerShell keeps giving errors, use Command Prompt (CMD):

1. Press `Windows + R`
2. Type `cmd` and press Enter
3. Run:
```cmd
cd "C:\Users\Mohanad alotaibe\Desktop\Lwaah"
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py runserver
```

---

**Follow these steps and the camera WILL work!** 🚀


