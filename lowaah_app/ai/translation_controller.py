"""
Translation Controller - Main orchestrator for sign language system
Coordinates all AI components for end-to-end translation.

Flow:
1. Video input → Sign recognition → Text
2. Text → Intent recognition → Service routing
3. Response → Text-to-sign → Avatar animation
"""

import numpy as np
from typing import Dict, Optional
import time


class TranslationController:
    """
    Main controller that coordinates all sign language AI components.
    """
    
    def __init__(self, use_lstm: bool = True):
        """
        Initialize translation controller with all AI components.
        
        Args:
            use_lstm: Whether to use LSTM model for sequence recognition
        """
        print("🚀 Initializing Translation Controller...")
        
        # Initialize components
        from .sign_sequence_recognizer import SignSequenceRecognizer
        from .intent_recognizer import IntentRecognizer
        from .text_to_sign_translator import TextToSignTranslator
        
        self.sign_recognizer = SignSequenceRecognizer(use_lstm=use_lstm)
        self.intent_recognizer = IntentRecognizer()
        self.text_to_sign = TextToSignTranslator()
        
        # State management
        self.session_state = {
            'current_text': '',
            'last_intent': None,
            'conversation_history': []
        }
        
        print("✅ Translation Controller ready!")
    
    def process_frame(self, image: np.ndarray) -> Dict:
        """
        Process a single video frame for continuous sign recognition.
        
        Args:
            image: Input frame (BGR format)
            
        Returns:
            Dictionary with recognition results and UI updates
        """
        # Recognize sign from frame
        recognition_result = self.sign_recognizer.recognize_continuous(image)
        
        response = {
            'success': True,
            'current_sign': recognition_result.get('sign'),
            'confidence': recognition_result.get('confidence', 0.0),
            'recognized_text': recognition_result.get('text', ''),
            'status': recognition_result.get('status'),
            'word_added': recognition_result.get('word_added', False)
        }
        
        # If a word was confirmed, update session
        if recognition_result.get('word_added'):
            self.session_state['current_text'] = recognition_result['text']
            
            # Try to recognize intent from accumulated text
            intent_result = self.intent_recognizer.recognize_intent(
                self.session_state['current_text']
            )
            
            response['intent'] = intent_result
            self.session_state['last_intent'] = intent_result
        
        return response
    
    def translate_sign_to_text(self, video_frames: list) -> Dict:
        """
        Translate a sequence of video frames to text.
        
        Args:
            video_frames: List of video frames
            
        Returns:
            Translation result with text and intent
        """
        # Process all frames
        for frame in video_frames:
            self.sign_recognizer.add_frame(frame)
        
        # Get final prediction
        predicted_text = self.sign_recognizer.current_text
        
        if not predicted_text:
            return {
                'success': False,
                'error': 'No text recognized',
                'text': ''
            }
        
        # Recognize intent
        intent_result = self.intent_recognizer.recognize_intent(predicted_text)
        
        return {
            'success': True,
            'text': predicted_text,
            'intent': intent_result,
            'confidence': 0.85  # Average confidence
        }
    
    def translate_text_to_sign(self, text: str) -> Dict:
        """
        Translate text to sign language animation.
        
        Args:
            text: Input text (Arabic or English)
            
        Returns:
            Animation data for 3D avatar
        """
        translation = self.text_to_sign.translate(text)
        
        if not translation['success']:
            return {
                'success': False,
                'error': translation.get('error')
            }
        
        # Export for avatar
        avatar_data = self.text_to_sign.export_for_avatar(translation)
        
        return {
            'success': True,
            'text': text,
            'animation_data': avatar_data,
            'duration': translation['total_duration'],
            'signs_count': len(translation['signs'])
        }
    
    def process_service_request(self, text: str) -> Dict:
        """
        Process a complete service request from sign language.
        
        Flow:
        1. Recognize intent from text
        2. Route to appropriate service
        3. Generate response
        4. Translate response to sign language
        
        Args:
            text: Recognized text from signs
            
        Returns:
            Complete response with routing and animation
        """
        start_time = time.time()
        
        # Step 1: Recognize intent
        intent_result = self.intent_recognizer.recognize_intent(text)
        
        if intent_result['confidence'] < 0.5:
            return {
                'success': False,
                'error': 'Unable to understand request',
                'suggestion': 'Please try again with clearer signs'
            }
        
        # Step 2: Generate response text
        response_text = self._generate_response_text(intent_result)
        
        # Step 3: Translate response to signs
        sign_animation = self.translate_text_to_sign(response_text)
        
        # Step 4: Get suggested actions
        actions = self.intent_recognizer.get_suggested_actions(intent_result['intent'])
        
        processing_time = time.time() - start_time
        
        return {
            'success': True,
            'input_text': text,
            'intent': intent_result,
            'response_text': response_text,
            'sign_animation': sign_animation.get('animation_data'),
            'actions': actions,
            'navigation_url': intent_result['url'],
            'processing_time': processing_time
        }
    
    def _generate_response_text(self, intent_result: Dict) -> str:
        """
        Generate appropriate response text based on intent.
        
        Args:
            intent_result: Intent recognition result
            
        Returns:
            Response text in Arabic
        """
        intent = intent_result['intent']
        service_name = intent_result.get('text_ar', '')
        
        # Generate contextual response
        responses = {
            'violations_inquiry': f'سأفتح لك {service_name}. يمكنك الاستعلام عن المخالفات باستخدام رقم اللوحة',
            'id_renewal': f'سأنتقل إلى {service_name}. يرجى تحضير المستندات المطلوبة',
            'license_renewal': f'جاري فتح {service_name}. ستحتاج إلى الفحص الطبي',
            'passport_issuance': f'سأفتح لك {service_name}. يمكنك متابعة الطلب',
            'profile': 'سأعرض لك الملف الشخصي',
            'services': 'سأعرض لك قائمة الخدمات المتاحة',
            'absher_individuals': 'مرحبا بك في أبشر أفراد',
        }
        
        return responses.get(intent, f'سأفتح لك {service_name}')
    
    def clear_session(self):
        """Clear current session state."""
        self.sign_recognizer.clear_text()
        self.session_state = {
            'current_text': '',
            'last_intent': None,
            'conversation_history': []
        }
        print("🧹 Session cleared")
    
    def delete_last_word(self):
        """Delete last recognized word."""
        self.sign_recognizer.delete_last_word()
        self.session_state['current_text'] = self.sign_recognizer.current_text
    
    def get_session_info(self) -> Dict:
        """Get current session information."""
        return {
            'current_text': self.session_state['current_text'],
            'last_intent': self.session_state['last_intent'],
            'conversation_history': self.session_state['conversation_history']
        }
    
    def add_to_conversation(self, user_text: str, system_response: str):
        """Add exchange to conversation history."""
        self.session_state['conversation_history'].append({
            'user': user_text,
            'system': system_response,
            'timestamp': time.time()
        })
    
    def get_system_status(self) -> Dict:
        """Get system component status."""
        return {
            'sign_recognizer': 'ready',
            'intent_recognizer': 'ready',
            'text_to_sign': 'ready',
            'lstm_available': self.sign_recognizer.use_lstm,
            'vocabulary_size': len(self.text_to_sign.sign_database),
            'session_active': len(self.session_state['current_text']) > 0
        }


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_controller_instance = None

def get_translation_controller(use_lstm: bool = True) -> TranslationController:
    """
    Get or create singleton translation controller instance.
    
    Args:
        use_lstm: Whether to use LSTM model
        
    Returns:
        TranslationController instance
    """
    global _controller_instance
    
    if _controller_instance is None:
        _controller_instance = TranslationController(use_lstm=use_lstm)
    
    return _controller_instance


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    """Test translation controller."""
    print("=" * 60)
    print("Translation Controller Test")
    print("=" * 60)
    
    # Create controller
    controller = TranslationController(use_lstm=False)
    
    # Test text-to-sign
    print("\n📝 Testing Text-to-Sign Translation...")
    test_texts = [
        "استعلام عن المخالفات",
        "تجديد الهوية",
        "صباح الخير"
    ]
    
    for text in test_texts:
        print(f"\n   Text: {text}")
        result = controller.translate_text_to_sign(text)
        if result['success']:
            print(f"   ✅ Success! Duration: {result['duration']:.1f}s")
        else:
            print(f"   ❌ Error: {result.get('error')}")
    
    # Test service request processing
    print("\n\n🎯 Testing Service Request Processing...")
    request_text = "أريد الاستعلام عن المخالفات"
    result = controller.process_service_request(request_text)
    
    if result['success']:
        print(f"   ✅ Request processed successfully!")
        print(f"   Intent: {result['intent']['intent']}")
        print(f"   Confidence: {result['intent']['confidence']:.2f}")
        print(f"   Response: {result['response_text']}")
        print(f"   URL: {result['navigation_url']}")
        print(f"   Processing time: {result['processing_time']*1000:.0f}ms")
    else:
        print(f"   ❌ Error: {result.get('error')}")
    
    # Show system status
    print("\n\n📊 System Status:")
    status = controller.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ Test Complete")
    print("=" * 60)


