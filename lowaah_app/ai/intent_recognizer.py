"""
Intent Recognition Engine for Absher Services
Uses NLP techniques to understand user intent from translated text.

Approaches:
1. Keyword matching (fast, rule-based)
2. Pattern matching (regex-based)
3. Semantic similarity (optional: sentence transformers)
"""

import re
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher


class IntentRecognizer:
    """
    Recognizes user intent from Arabic text for Absher services.
    """
    
    def __init__(self):
        """Initialize intent recognizer with Absher service patterns."""
        from .sign_language_vocabulary import (
            INTENT_TO_SERVICE, 
            ABSHER_SERVICES,
            ACTION_VERBS,
            QUESTION_WORDS
        )
        
        self.intent_to_service = INTENT_TO_SERVICE
        self.services_vocab = ABSHER_SERVICES
        self.actions_vocab = ACTION_VERBS
        self.questions_vocab = QUESTION_WORDS
        
        # Define intent patterns (Arabic text patterns)
        self.intent_patterns = self._build_intent_patterns()
        
        print("✅ IntentRecognizer initialized with Absher services")
    
    def _build_intent_patterns(self) -> Dict[str, List[str]]:
        """
        Build regex patterns for each intent.
        
        Returns:
            Dictionary mapping intent names to regex patterns
        """
        patterns = {
            'violations_inquiry': [
                r'(استعلام|استفسار|بحث).*(مخالفات|مخالفة)',
                r'مخالفات.*(سيارة|لوحة)',
                r'(عرض|اعرض|شوف|أرى).*(مخالفات)',
                r'(كم|هل).*(مخالفة|مخالفات)',
                r'مخالفات',  # Simple keyword
            ],
            'id_renewal': [
                r'(تجديد|جدد|تحديث).*(هوية|بطاقة)',
                r'هوية.*(جديد|تجديد|منتهية)',
                r'(أريد|أرغب).*(تجديد).*(هوية)',
                r'تجديد.*هوية',
            ],
            'license_renewal': [
                r'(تجديد|جدد).*(رخصة|رخصه).*(قيادة)',
                r'رخصة.*(قيادة).*(تجديد|منتهية)',
                r'(أريد|أرغب).*(تجديد).*(رخصة)',
                r'رخصة.*قيادة',
            ],
            'passport_issuance': [
                r'(استخراج|إصدار|جديد).*(جواز|باسبور).*(سفر)',
                r'جواز.*(سفر).*(جديد|استخراج)',
                r'(أريد|أحتاج).*(جواز).*(سفر)',
                r'جواز.*سفر',
            ],
            'visa_services': [
                r'(تأشيرة|فيزا|تاشيره)',
                r'(استخراج|تجديد).*(تأشيرة)',
                r'(تأشيرة).*(خروج|دخول|عمل|زيارة)',
            ],
            'residence_services': [
                r'(إقامة|اقامه)',
                r'(تجديد|استخراج).*(إقامة)',
                r'(مقيم|مقيمين)',
            ],
            'appointment_booking': [
                r'(موعد|حجز)',
                r'(أريد|أحتاج).*(موعد)',
                r'(حجز|احجز).*(موعد)',
            ],
            'payment_services': [
                r'(دفع|سداد|ادفع)',
                r'(دفع|سداد).*(غرامة|فاتورة|مخالفة)',
                r'(أريد|أرغب).*(دفع|سداد)',
            ],
            'certificates': [
                r'(شهادة)',
                r'(شهادة).*(ميلاد|وفاة|زواج|طلاق)',
                r'(استخراج|طلب).*(شهادة)',
            ],
            'work_services': [
                r'(عمل|وظيفة)',
                r'(تصريح).*(عمل)',
                r'(عقد).*(عمل)',
            ],
            'health_services': [
                r'(صحي|طبي|تأمين)',
                r'(مستشفى|علاج)',
                r'(تأمين).*(صحي)',
            ],
            'profile': [
                r'(ملف|بروفايل|حساب).*(شخصي)',
                r'(عرض|افتح|شوف).*(ملف|حساب)',
                r'(معلومات|بيانات).*(شخصية)',
            ],
            'absher_individuals': [
                r'(أبشر|ابشر).*(أفراد|افراد)',
                r'(خدمات|خدمة).*(أفراد)',
            ],
            'services': [
                r'(خدمات|الخدمات)',
                r'(قائمة|عرض).*(خدمات)',
                r'(جميع|كل).*(خدمات)',
            ],
            'help': [
                r'(مساعدة|ساعدني|مساعده)',
                r'(كيف|ازاي|وش)',
                r'(شرح|اشرح)',
            ],
        }
        
        return patterns
    
    def recognize_intent(self, text: str) -> Dict:
        """
        Recognize intent from Arabic text.
        
        Args:
            text: Input text (Arabic)
            
        Returns:
            Dictionary with intent, confidence, and service info
        """
        if not text or len(text.strip()) == 0:
            return self._create_result('unknown', 0.0, None)
        
        text_clean = text.strip().lower()
        
        # Step 1: Pattern matching
        pattern_result = self._match_patterns(text_clean)
        if pattern_result['confidence'] > 0.7:
            return pattern_result
        
        # Step 2: Keyword matching
        keyword_result = self._match_keywords(text_clean)
        if keyword_result['confidence'] > 0.6:
            return keyword_result
        
        # Step 3: Fuzzy matching (fallback)
        fuzzy_result = self._fuzzy_match(text_clean)
        if fuzzy_result['confidence'] > 0.5:
            return fuzzy_result
        
        # Default: services page
        return self._create_result('services', 0.3, 
                                   self.intent_to_service.get('services'))
    
    def _match_patterns(self, text: str) -> Dict:
        """Match text against intent patterns."""
        best_intent = None
        best_score = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Calculate confidence based on pattern specificity
                    specificity = len(pattern) / 100.0  # Longer patterns = more specific
                    confidence = min(0.95, 0.7 + specificity)
                    
                    if confidence > best_score:
                        best_score = confidence
                        best_intent = intent
        
        if best_intent:
            service = self.intent_to_service.get(best_intent)
            return self._create_result(best_intent, best_score, service)
        
        return self._create_result('unknown', 0.0, None)
    
    def _match_keywords(self, text: str) -> Dict:
        """Match text against service keywords."""
        words = text.split()
        intent_scores = {}
        
        # Count keyword matches for each intent
        for word in words:
            # Check services vocabulary
            if word in self.services_vocab:
                intent = self.services_vocab[word].get('intent', '')
                intent_scores[intent] = intent_scores.get(intent, 0) + 1
        
        if not intent_scores:
            return self._create_result('unknown', 0.0, None)
        
        # Get best intent
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(0.9, 0.5 + (intent_scores[best_intent] * 0.1))
        
        # Map to service intent
        intent_mapping = {
            'violations': 'violations_inquiry',
            'identity': 'id_renewal',
            'license': 'license_renewal',
            'passport': 'passport_issuance',
            'visa': 'visa_services',
            'residence': 'residence_services',
        }
        
        mapped_intent = intent_mapping.get(best_intent, 'services')
        service = self.intent_to_service.get(mapped_intent)
        
        return self._create_result(mapped_intent, confidence, service)
    
    def _fuzzy_match(self, text: str) -> Dict:
        """Fuzzy matching against known service names."""
        best_match = None
        best_ratio = 0.0
        
        for intent, service in self.intent_to_service.items():
            service_name = service['service_name'].lower()
            ratio = SequenceMatcher(None, text, service_name).ratio()
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = intent
        
        if best_ratio > 0.5:
            service = self.intent_to_service.get(best_match)
            return self._create_result(best_match, best_ratio, service)
        
        return self._create_result('unknown', 0.0, None)
    
    def _create_result(self, intent: str, confidence: float, 
                       service: Optional[Dict]) -> Dict:
        """Create standardized result dictionary."""
        result = {
            'intent': intent,
            'confidence': confidence,
            'service': service,
            'text_ar': service['service_name'] if service else '',
            'text_en': service['service_name_en'] if service else '',
            'url': service['url'] if service else '/services/',
            'actions': service['actions'] if service else []
        }
        
        return result
    
    def extract_entities(self, text: str) -> Dict:
        """
        Extract entities from text (e.g., ID numbers, dates, names).
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {
            'national_id': [],
            'plate_number': [],
            'date': [],
            'phone': [],
            'email': []
        }
        
        # Extract National ID (10 digits)
        id_pattern = r'\b\d{10}\b'
        entities['national_id'] = re.findall(id_pattern, text)
        
        # Extract plate number (1-4 digits)
        plate_pattern = r'\b\d{1,4}\b'
        entities['plate_number'] = re.findall(plate_pattern, text)
        
        # Extract phone number (Saudi format)
        phone_pattern = r'(05|5)\d{8}'
        entities['phone'] = re.findall(phone_pattern, text)
        
        # Extract dates (basic patterns)
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        entities['date'] = re.findall(date_pattern, text)
        
        return entities
    
    def get_suggested_actions(self, intent: str) -> List[Dict]:
        """
        Get suggested actions for a given intent.
        
        Args:
            intent: Intent name
            
        Returns:
            List of suggested actions with details
        """
        service = self.intent_to_service.get(intent)
        
        if not service:
            return []
        
        actions = []
        for action_key in service.get('actions', []):
            action_info = self._get_action_details(action_key)
            actions.append(action_info)
        
        return actions
    
    def _get_action_details(self, action_key: str) -> Dict:
        """Get detailed information for an action."""
        action_map = {
            'query_violations': {
                'key': 'query_violations',
                'name_ar': 'الاستعلام عن المخالفات',
                'name_en': 'Query Violations',
                'icon': '🔍',
                'requires': ['plate_number']
            },
            'pay_fine': {
                'key': 'pay_fine',
                'name_ar': 'دفع الغرامة',
                'name_en': 'Pay Fine',
                'icon': '💳',
                'requires': ['violation_id']
            },
            'renew_id': {
                'key': 'renew_id',
                'name_ar': 'تجديد الهوية',
                'name_en': 'Renew ID',
                'icon': '🆔',
                'requires': ['national_id']
            },
            'renew_license': {
                'key': 'renew_license',
                'name_ar': 'تجديد رخصة القيادة',
                'name_en': 'Renew License',
                'icon': '🚗',
                'requires': ['license_number']
            },
            'apply_passport': {
                'key': 'apply_passport',
                'name_ar': 'طلب جواز سفر',
                'name_en': 'Apply for Passport',
                'icon': '🛂',
                'requires': ['national_id']
            },
            'view_profile': {
                'key': 'view_profile',
                'name_ar': 'عرض الملف الشخصي',
                'name_en': 'View Profile',
                'icon': '👤',
                'requires': []
            },
            'browse_services': {
                'key': 'browse_services',
                'name_ar': 'تصفح الخدمات',
                'name_en': 'Browse Services',
                'icon': '📋',
                'requires': []
            },
        }
        
        return action_map.get(action_key, {
            'key': action_key,
            'name_ar': action_key,
            'name_en': action_key,
            'icon': '⚙️',
            'requires': []
        })


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def test_intent_recognition():
    """Test the intent recognizer with sample queries."""
    recognizer = IntentRecognizer()
    
    test_queries = [
        "أريد الاستعلام عن المخالفات",
        "تجديد الهوية",
        "رخصة القيادة",
        "جواز سفر جديد",
        "افتح الملف الشخصي",
        "خدمات أبشر",
        "دفع غرامة",
        "شهادة ميلاد",
    ]
    
    print("\n" + "="*60)
    print("Testing Intent Recognition")
    print("="*60)
    
    for query in test_queries:
        result = recognizer.recognize_intent(query)
        print(f"\n📝 Query: {query}")
        print(f"   Intent: {result['intent']}")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Service: {result['text_ar']} ({result['text_en']})")
        print(f"   URL: {result['url']}")


if __name__ == "__main__":
    test_intent_recognition()


