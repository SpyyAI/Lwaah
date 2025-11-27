# 🤚 Lowaah - Complete Gesture Guide

## 📋 Available Gestures

### Navigation Gestures
| Gesture | Action | How to Perform |
|---------|--------|----------------|
| ✋ **Open Hand** | Navigate to Services | Spread all 5 fingers wide apart |
| ✊ **Closed Fist** | Violations Inquiry | Close all fingers including thumb tightly |
| ✌️ **Victory Sign** | Absher Individuals | Extend index + middle fingers only |
| 👉 **Palm Right** | Navigate Right | Move hand to the right side |
| 👈 **Palm Left** | Navigate Left | Move hand to the left side |

### Form Control Gestures
| Gesture | Action | How to Perform |
|---------|--------|----------------|
| 👍 **Thumbs Up** | Next Field / Submit | Thumb extended upward, all fingers closed |
| 👎 **Thumbs Down** | Previous Field / Go Back | Thumb pointing downward, all fingers closed |
| ☝️ **Pointing Index** | Select / Focus Field | Only index finger extended |

### Special Gestures
| Gesture | Action | How to Perform |
|---------|--------|----------------|
| 🤙 **Pinky Extended** | Backspace/Delete | Only pinky finger extended |

---

## 🎯 Complete User Journey: Violations Inquiry

### Step 1: Navigate to Violations Page
1. **Start at home page** (`http://127.0.0.1:8000/`)
2. **Click camera button** (📹) to enable gesture control
3. **Show ✊ Closed Fist** gesture
4. **Wait for navigation** (you'll be taken to `/violations/`)

### Step 2: Enter ID Number
1. **Show ☝️ Pointing Index** to select first field (ID Number)
2. **Type numbers using keyboard** (or use on-screen keyboard)
3. **Show 👍 Thumbs Up** to move to next field

### Step 3: Enter Plate Number
1. **Field auto-focused** (thanks to thumbs up)
2. **Type plate number using keyboard**
3. **Show 👍 Thumbs Up** to submit form

### Step 4: View Results
1. **Results appear automatically**
2. **Show 👍 Thumbs Up** to pay all violations
3. **Confirmation page appears**

---

## ⚙️ Gesture Detection Settings

### Confidence Threshold
- **Current**: 0.5 (50%)
- Gestures must be detected with at least 50% confidence

### Consecutive Detections
- **Required**: 2 consecutive detections
- Prevents accidental triggers
- Hold gesture steady for ~1-2 seconds

### Cooldown Period
- **Duration**: 3 seconds
- Prevents repeated actions from same gesture
- Wait 3 seconds before repeating the same gesture

---

## 💡 Tips for Best Performance

### ✅ DO:
- **Good lighting** - Face a window or bright light source
- **Hand fully visible** - Keep entire hand within camera frame
- **Hold steady** - Maintain gesture for 2-3 seconds
- **Clear gestures** - Make distinct, deliberate poses
- **Face camera** - Keep palm facing toward camera

### ❌ DON'T:
- **Avoid shadows** - Don't have backlight
- **No fast movements** - Hold gestures steady
- **Don't partially hide** - Keep all fingers visible
- **Avoid similar gestures** - Wait for confirmation before changing

---

## 🔧 Troubleshooting

### Closed Fist Not Detected
**Problem**: Detected as thumbs_up or other gesture

**Solution**:
1. Make sure **thumb is completely closed** against palm
2. Close **all 4 fingers tightly**
3. Make a **very tight fist**
4. Hold for **2-3 seconds**

### Thumbs Up Confused with Fist
**Problem**: Both detect as same gesture

**Solution**: 
1. For thumbs up: **Thumb must point UP** (toward ceiling)
2. For fist: **Thumb must be tucked IN** (against palm)
3. **Exaggerate** the difference

---

## 🎮 Practice Mode

Visit the **test camera page** to practice:
```
http://127.0.0.1:8000/test-camera/
```

Features:
- ✅ Live gesture detection
- ✅ Confidence scores
- ✅ Debug logs
- ✅ Visual feedback

---

## 📊 Gesture Priority Order

The system checks gestures in this order:

1. **Backspace** (highest priority - very specific)
2. **Closed Fist** (checked early to avoid confusion)
3. **Thumbs Up/Down** (very specific)
4. **Victory Sign** (specific)
5. **Pointing Index** (specific)
6. **Open Hand** (less specific)
7. **Palm Movement** (least specific - checked last)

This order prevents gesture confusion!

---

## 🚀 Future Enhancements

### Coming Soon:
- ✅ **Arabic letter signs** for text input
- ✅ **Voice feedback** when gesture detected
- ✅ **Backspace gesture** to delete characters
- ✅ **Custom gesture training** for personalization
- ✅ **Multi-hand gestures** for complex commands

---

## 📝 Notes

- **Browser Support**: Chrome, Edge (requires WebRTC)
- **Camera Permission**: Required on first use
- **Performance**: 60ms processing time per frame
- **Accuracy**: ~85-95% with good lighting
- **Languages**: Arabic & English UI

---

**Made with ❤️ for accessibility in Saudi Arabia** 🇸🇦

