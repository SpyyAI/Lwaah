# 📖 Usage Examples - Sign Language Translation System

## Real-World Scenarios

---

## Scenario 1: Check Traffic Violations 🚗

### User Story
Ahmed received an SMS about a traffic violation. He wants to check the details using sign language.

### Steps

1. **Access System**
   ```
   User navigates to: http://127.0.0.1:8000/
   User clicks: 🤟 icon in header
   ```

2. **Sign the Query**
   ```
   User signs:
   - "استعلام" (inquiry) → pointing forward gesture
   - "عن" (about) → connecting gesture  
   - "المخالفات" (violations) → warning gesture
   ```

3. **System Response**
   ```
   Recognized Text: "استعلام عن المخالفات"
   Intent: violations_inquiry (confidence: 92%)
   Action: Navigate to /violations/
   ```

4. **Avatar Response**
   ```
   Avatar signs: "سأفتح لك الاستعلام عن المخالفات"
   (I will open violations inquiry for you)
   ```

5. **Complete Transaction**
   ```
   System navigates to violations page
   User enters plate number
   System displays violations
   ```

---

## Scenario 2: Renew National ID 🆔

### User Story
Fatima's ID is expiring soon. She wants to renew it using sign language.

### Steps

1. **Sign the Request**
   ```
   User signs:
   - "تجديد" (renewal) → circular rotating gesture
   - "الهوية" (ID) → card-showing gesture
   ```

2. **System Understanding**
   ```
   Recognized Text: "تجديد الهوية"
   Intent: id_renewal (confidence: 88%)
   Suggested Actions:
   - Renew ID
   - Upload Documents
   - Check Status
   ```

3. **Avatar Confirmation**
   ```
   Avatar signs: "سأنتقل إلى تجديد الهوية. يرجى تحضير المستندات"
   (I will go to ID renewal. Please prepare documents)
   ```

4. **Navigation**
   ```
   System navigates to /id-renewal/
   Shows renewal form
   Lists required documents
   ```

---

## Scenario 3: Book Appointment 📅

### User Story
Mohammed needs to book an appointment at a government office.

### Signs Sequence
```
"أريد" + "حجز" + "موعد"
(I want) + (book) + (appointment)
```

### System Processing
```
Input: "أريد حجز موعد"
Intent: appointment_booking (confidence: 85%)
Navigation: /appointments/
Actions: [Select Service, Choose Date, Confirm]
```

---

## Scenario 4: Pay Fine 💳

### User Story
Sara needs to pay a parking fine.

### Signs Sequence
```
"دفع" + "غرامة"
(pay) + (fine)
```

### System Processing
```
Input: "دفع غرامة"
Intent: payment_services (confidence: 90%)
Features Extracted:
- Action: payment
- Target: fine
Navigation: /payments/
```

---

## Code Examples

### Example 1: Manual Translation (JavaScript)

```javascript
// Translate Arabic text to sign language
async function demonstrateTranslation() {
    const text = "استعلام عن المخالفات";
    
    const result = await signTranslator.translateTextToSign(text);
    
    if (result.success) {
        console.log(`✅ Translation successful`);
        console.log(`Duration: ${result.duration}s`);
        console.log(`Signs: ${result.signs_count}`);
        
        // Avatar will automatically perform the signs
    }
}

demonstrateTranslation();
```

### Example 2: Process Custom Request (JavaScript)

```javascript
// Process a custom service request
async function processCustomRequest() {
    const userText = "أريد تجديد رخصة القيادة";
    
    const response = await fetch('/api/translate/process-request/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: userText })
    });
    
    const result = await response.json();
    
    if (result.success) {
        console.log('Intent:', result.intent.intent);
        console.log('Service:', result.intent.text_ar);
        console.log('URL:', result.navigation_url);
        console.log('Actions:', result.actions);
        
        // Navigate to service
        window.location.href = result.navigation_url;
    }
}
```

### Example 3: Custom Sign Recognition (Python)

```python
# Test sign recognition with custom video
import cv2
from lowaah_app.ai.translation_controller import get_translation_controller

# Initialize controller
controller = get_translation_controller()

# Open video file
video = cv2.VideoCapture('my_signs_video.mp4')

# Process frames
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    
    # Process frame
    result = controller.process_frame(frame)
    
    if result['word_added']:
        print(f"✅ Recognized word: {result['current_sign']}")
        print(f"   Full text: {result['recognized_text']}")
        print(f"   Confidence: {result['confidence']:.2f}")

# Get final text
session_info = controller.get_session_info()
print(f"\n📝 Final text: {session_info['current_text']}")
```

### Example 4: Add Custom Vocabulary (Python)

```python
# Add custom signs to vocabulary
from lowaah_app.ai.sign_language_vocabulary import COMPLETE_VOCABULARY

# Add new service sign
COMPLETE_VOCABULARY['تأمين_صحي'] = {
    'type': 'phrase',
    'text': 'تأمين صحي',
    'english': 'health insurance',
    'category': 'service_phrase',
    'intent': 'health_insurance'
}

# Add to intent mapping
from lowaah_app.ai.sign_language_vocabulary import INTENT_TO_SERVICE

INTENT_TO_SERVICE['health_insurance'] = {
    'url': '/health-insurance/',
    'service_name': 'التأمين الصحي',
    'service_name_en': 'Health Insurance',
    'actions': ['view_policy', 'file_claim', 'renew_insurance']
}

print("✅ Custom vocabulary added!")
```

---

## API Usage Examples

### Example 1: Sign-to-Text API

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/translate/sign-to-text/ \
  -H "Content-Type: application/json" \
  -d '{
    "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  }'
```

**Response**:
```json
{
  "success": true,
  "current_sign": "استعلام",
  "confidence": 0.92,
  "recognized_text": "استعلام عن المخالفات",
  "status": "confirmed",
  "word_added": true,
  "intent": {
    "intent": "violations_inquiry",
    "confidence": 0.88,
    "text_ar": "الاستعلام عن المخالفات",
    "text_en": "Violations Inquiry",
    "url": "/violations/"
  }
}
```

### Example 2: Text-to-Sign API

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/translate/text-to-sign/ \
  -H "Content-Type: application/json" \
  -d '{"text": "صباح الخير"}'
```

**Response**:
```json
{
  "success": true,
  "text": "صباح الخير",
  "animation_data": "{\"version\":\"1.0\",\"signs\":[...]}",
  "duration": 2.0,
  "signs_count": 2
}
```

### Example 3: System Status Check

**Request**:
```bash
curl http://127.0.0.1:8000/api/translate/status/
```

**Response**:
```json
{
  "status": "operational",
  "components": {
    "sign_recognizer": "ready",
    "intent_recognizer": "ready",
    "text_to_sign": "ready",
    "lstm_available": false,
    "vocabulary_size": 200,
    "session_active": true
  }
}
```

---

## Testing Scripts

### Test Script 1: Complete Workflow

```python
"""
Test complete sign-to-text-to-sign workflow
"""
import requests
import cv2
import base64
import time

# Configuration
API_BASE = "http://127.0.0.1:8000/api/translate"

def test_complete_workflow():
    print("="*60)
    print("Testing Complete Sign Language Translation Workflow")
    print("="*60)
    
    # Step 1: Capture frame
    print("\n1. Capturing video frame...")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("❌ Failed to capture frame")
        return
    
    # Convert to base64
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    print("✅ Frame captured")
    
    # Step 2: Sign-to-text
    print("\n2. Translating sign to text...")
    response = requests.post(
        f"{API_BASE}/sign-to-text/",
        json={"frame": f"data:image/jpeg;base64,{frame_base64}"}
    )
    result = response.json()
    
    if result['success']:
        print(f"✅ Recognized: {result.get('current_sign', 'None')}")
        print(f"   Text: {result.get('recognized_text', '')}")
        print(f"   Confidence: {result.get('confidence', 0)*100:.0f}%")
    
    # Step 3: Process request
    if result.get('recognized_text'):
        print("\n3. Processing service request...")
        response = requests.post(
            f"{API_BASE}/process-request/",
            json={"text": result['recognized_text']}
        )
        service_result = response.json()
        
        if service_result['success']:
            print(f"✅ Intent: {service_result['intent']['intent']}")
            print(f"   Service: {service_result['intent']['text_ar']}")
            print(f"   URL: {service_result['navigation_url']}")
    
    # Step 4: Text-to-sign
    print("\n4. Translating response to sign language...")
    response = requests.post(
        f"{API_BASE}/text-to-sign/",
        json={"text": "سأفتح لك الخدمة"}
    )
    sign_result = response.json()
    
    if sign_result['success']:
        print(f"✅ Animation generated")
        print(f"   Duration: {sign_result['duration']}s")
        print(f"   Signs: {sign_result['signs_count']}")
    
    # Step 5: System status
    print("\n5. Checking system status...")
    response = requests.get(f"{API_BASE}/status/")
    status = response.json()
    
    print(f"✅ System Status: {status['status']}")
    for component, state in status['components'].items():
        print(f"   {component}: {state}")
    
    print("\n" + "="*60)
    print("✅ Workflow Test Complete!")
    print("="*60)

if __name__ == "__main__":
    test_complete_workflow()
```

### Test Script 2: Vocabulary Coverage

```python
"""
Test vocabulary coverage
"""
from lowaah_app.ai.sign_language_vocabulary import (
    ARABIC_LETTERS,
    NUMBERS,
    ABSHER_SERVICES,
    ACTION_VERBS,
    QUESTION_WORDS,
    COMMON_PHRASES
)

def test_vocabulary():
    print("="*60)
    print("Vocabulary Coverage Test")
    print("="*60)
    
    categories = {
        "Arabic Letters": ARABIC_LETTERS,
        "Numbers": NUMBERS,
        "Absher Services": ABSHER_SERVICES,
        "Action Verbs": ACTION_VERBS,
        "Question Words": QUESTION_WORDS,
        "Common Phrases": COMMON_PHRASES
    }
    
    total_signs = 0
    
    for category, signs in categories.items():
        count = len(signs)
        total_signs += count
        print(f"\n{category}: {count} signs")
        
        # Show sample
        sample = list(signs.items())[:3]
        for key, value in sample:
            english = value.get('english', value.get('text', ''))
            print(f"   - {key} → {english}")
    
    print(f"\n{'='*60}")
    print(f"Total Vocabulary: {total_signs} signs")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_vocabulary()
```

---

## Troubleshooting Examples

### Problem 1: Low Recognition Confidence

**Symptoms**:
```json
{
  "confidence": 0.45,
  "status": "uncertain"
}
```

**Solutions**:
```python
# 1. Improve lighting
# 2. Slow down signs
# 3. Hold sign longer (2+ seconds)
# 4. Use clearer hand gestures
# 5. Retrain model with more data
```

### Problem 2: Wrong Intent Detected

**Symptoms**:
```json
{
  "intent": "services",
  "confidence": 0.35
}
```

**Solutions**:
```python
# Add more specific keywords to intent patterns
from lowaah_app.ai.intent_recognizer import IntentRecognizer

recognizer = IntentRecognizer()

# Add custom pattern
recognizer.intent_patterns['my_service'] = [
    r'(custom|pattern).*keywords',
]
```

### Problem 3: Avatar Not Animating

**Check**:
```javascript
// 1. Check if Three.js loaded
if (typeof THREE === 'undefined') {
    console.error('Three.js not loaded!');
}

// 2. Check avatar initialization
if (signTranslator.avatar) {
    console.log('✅ Avatar initialized');
} else {
    console.error('❌ Avatar not initialized');
}

// 3. Check animation data
console.log('Animation data:', result.sign_animation);
```

---

## Performance Optimization

### Optimize Frame Rate

```javascript
// Reduce processing frequency for better performance
signTranslator.frameRate = 5; // Process 5 frames per second instead of 10
```

### Batch Processing

```python
# Process multiple frames in batch
from lowaah_app.ai.translation_controller import get_translation_controller

controller = get_translation_controller()
frames = [frame1, frame2, frame3]  # List of frames

for frame in frames:
    controller.sign_recognizer.add_frame(frame)

# Get final prediction after all frames
text = controller.sign_recognizer.current_text
```

---

## 🎉 Success Stories

### Example 1: Complete Service Request
```
✅ User signed: "استعلام عن المخالفات"
✅ System recognized with 92% confidence
✅ Navigated to violations page
✅ User completed task in 45 seconds
```

### Example 2: Complex Query
```
✅ User signed: "أريد تجديد رخصة القيادة"
✅ System understood intent: license_renewal (88%)
✅ Showed required documents
✅ Booked appointment automatically
```

---

**Need more examples? Check the full documentation in `SIGN_LANGUAGE_TRANSLATION_SYSTEM.md`**

**Happy Signing! 🤟**


