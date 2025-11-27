"""
Quick test script to verify translation system components
Run this to diagnose issues with sign translation
"""

import os
import sys

print("="*60)
print("🔧 Translation System Diagnostic Test")
print("="*60)

# Check if files exist
print("\n1. Checking AI components...")
ai_files = [
    'lowaah_app/ai/sign_language_vocabulary.py',
    'lowaah_app/ai/sign_sequence_recognizer.py',
    'lowaah_app/ai/intent_recognizer.py',
    'lowaah_app/ai/text_to_sign_translator.py',
    'lowaah_app/ai/translation_controller.py',
]

for file in ai_files:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"   {status} {file}")

# Check frontend files
print("\n2. Checking frontend files...")
frontend_files = [
    'lowaah_app/static/js/sign-avatar.js',
    'lowaah_app/static/js/sign-translator.js',
    'lowaah_app/static/css/sign-translation.css',
]

for file in frontend_files:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    size = os.path.getsize(file) if exists else 0
    print(f"   {status} {file} ({size} bytes)")

# Test imports
print("\n3. Testing Python imports...")
try:
    from lowaah_app.ai.translation_controller import get_translation_controller
    print("   ✅ Translation controller imports successfully")
    
    controller = get_translation_controller(use_lstm=False)
    print("   ✅ Translation controller initializes")
    
    status = controller.get_system_status()
    print("   ✅ System status:")
    for key, value in status.items():
        print(f"      - {key}: {value}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test text-to-sign
print("\n4. Testing text-to-sign translation...")
try:
    result = controller.translate_text_to_sign("صباح الخير")
    if result['success']:
        print(f"   ✅ Translation successful!")
        print(f"      Duration: {result['duration']}s")
        print(f"      Signs: {result['signs_count']}")
    else:
        print(f"   ❌ Translation failed: {result.get('error')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("Diagnostic complete!")
print("="*60)

print("\n📝 Next Steps:")
print("1. If all checks pass → Issue is in the browser/frontend")
print("2. Check browser console for JavaScript errors")
print("3. Make sure you're clicking the 🤟 icon (NOT 📹)")
print("4. Clear browser cache and refresh (Ctrl+F5)")


