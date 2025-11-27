# 🎯 Lowaah Gesture System Documentation

## Overview
The Lowaah system uses **context-aware gestures** - the same gesture can perform different actions depending on which page you're on.

---

## 📋 How It Works

### 1. **Default Gesture Actions** (Home, Services, etc.)
These are the standard meanings when browsing the app:

| Gesture | Action | Description |
|---------|--------|-------------|
| 🖐️ **Open Hand** | Navigate to Services | Opens the services menu |
| ✊ **Closed Fist** | Navigate to Violations | Opens violations inquiry |
| 👍 **Thumbs Up** | Next/Approve/Submit | Moves forward or confirms |
| 👎 **Thumbs Down** | Back/Cancel | Goes back or cancels |
| ☝️ **Pointing Index** | Select/Focus | Selects current item |
| ✌️ **Victory Sign** | Navigate to Absher | Opens Absher Individuals |
| 👋 **Palm Right** | Navigate Right | Moves to next item |
| 👋 **Palm Left** | Navigate Left | Moves to previous item |

---

### 2. **Profile Selection Page** (Override Mode)
When you're on `/profile/select/`, gestures have special meanings:

| Gesture | Action | Description |
|---------|--------|-------------|
| ✊ **Closed Fist** | Select Profile 1 | Chooses the first profile |
| ✌️ **Victory Sign** | Select Profile 2 | Chooses the second profile |
| 🖐️ **Open Hand** | Select Profile 3 | Chooses the third profile |
| 👍 **Thumbs Up** | Create New Profile | Opens profile creation wizard |
| 👎 **Thumbs Down** | Go Back | Returns to previous page |

**Note:** On this page, gestures **do NOT** navigate to Services/Violations!

---

### 3. **Form Pages** (Context-Aware Actions)
On forms like violations inquiry:

| Gesture | Action | Description |
|---------|--------|-------------|
| 👍 **Thumbs Up** | Next Field/Submit | Moves to next input or submits |
| 👎 **Thumbs Down** | Previous Field/Back | Moves to previous input |
| ☝️ **Pointing Index** | Select/Focus Field | Focuses on current field |

---

## 🔧 Technical Implementation

### Page-Specific Gesture Override

Any page can override gesture behavior by defining `window.PAGE_GESTURE_HANDLERS`:

```javascript
// In your page's <script> tag
window.PAGE_GESTURE_HANDLERS = {
    'closed_fist': function() {
        console.log('Custom action for closed fist');
        // Your custom logic here
    },
    'thumbs_up': function() {
        console.log('Custom action for thumbs up');
        // Your custom logic here
    }
    // ... other gestures
};
```

### Detection Priority

1. **Check for `window.PAGE_GESTURE_HANDLERS`** - If defined, use page-specific handlers
2. **Fall back to `DEFAULT_GESTURE_ACTIONS`** - Use standard navigation if no override

### Cooldown System

- Each gesture has a **3-second cooldown** to prevent accidental repeated actions
- Requires **2 consecutive detections** before triggering (reduces false positives)

---

## 🎨 Visual Feedback

### On All Pages:
- **Gesture panel** shows detected gesture in real-time
- **Confidence bar** displays detection accuracy
- **Notification popup** appears when action is triggered

### On Profile Selection:
- **Profile cards** highlight when selected
- **Auto-confirmation** after 2 seconds
- **Visual indicators** show which gesture selects which profile

---

## 🐛 Debugging

### Check Current Gesture Mode:
Open browser console and type:
```javascript
console.log(window.PAGE_GESTURE_HANDLERS ? 'Page-specific mode' : 'Default mode');
```

### Test Gesture Detection:
```javascript
// Manually trigger a gesture
if (typeof handleGesture === 'function') {
    handleGesture('thumbs_up', 0.95);
}
```

### View Active Handlers:
```javascript
console.log(getGestureActions());
```

---

## ✅ Best Practices

1. **Always define page overrides BEFORE camera starts**
2. **Log actions** for debugging: `console.log('Action executed')`
3. **Provide visual feedback** so users know their gesture was recognized
4. **Use cooldowns** to prevent rapid-fire actions
5. **Clear overrides** when leaving the page (automatic with page reload)

---

## 📝 Adding New Pages with Custom Gestures

Example template:

```html
{% extends 'lowaah_app/base.html' %}

{% block content %}
    <!-- Your page content -->
{% endblock %}

{% block extra_js %}
<script>
    // Define custom gesture handlers
    window.PAGE_GESTURE_HANDLERS = {
        'open_hand': function() {
            // Custom action for this page
            alert('Custom action!');
        },
        'thumbs_up': function() {
            // Another custom action
            submitForm();
        }
    };
    
    console.log('✅ Custom gesture handlers registered');
</script>
{% endblock %}
```

---

## 🔍 Troubleshooting

### Problem: Gesture goes to wrong page
**Solution:** Check if page defines `window.PAGE_GESTURE_HANDLERS`. If not, it uses default navigation.

### Problem: Gesture not detected
**Solution:** 
- Check camera panel is open
- Ensure lighting is good
- Check console for detection messages
- Try holding gesture for 2 seconds

### Problem: Conflicts between pages
**Solution:** Each page override only applies to that page. Reloading clears overrides.

---

**Last Updated:** November 23, 2025  
**Version:** 2.0 (Context-Aware System)


