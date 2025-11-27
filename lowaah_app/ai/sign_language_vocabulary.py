"""
Sign Language Vocabulary Database
Comprehensive mapping of Saudi Sign Language (KSL) signs to Arabic/English text.

Covers:
- Arabic alphabet (28 letters)
- Numbers (0-9)
- Common words and phrases
- Absher service keywords
- Action verbs
- Question words
"""

# ============================================================================
# ARABIC ALPHABET SIGNS (Finger Spelling)
# ============================================================================

ARABIC_LETTERS = {
    'أ': {'english': 'alif', 'category': 'letter'},
    'ب': {'english': 'ba', 'category': 'letter'},
    'ت': {'english': 'ta', 'category': 'letter'},
    'ث': {'english': 'tha', 'category': 'letter'},
    'ج': {'english': 'jeem', 'category': 'letter'},
    'ح': {'english': 'ha', 'category': 'letter'},
    'خ': {'english': 'kha', 'category': 'letter'},
    'د': {'english': 'dal', 'category': 'letter'},
    'ذ': {'english': 'thal', 'category': 'letter'},
    'ر': {'english': 'ra', 'category': 'letter'},
    'ز': {'english': 'zay', 'category': 'letter'},
    'س': {'english': 'seen', 'category': 'letter'},
    'ش': {'english': 'sheen', 'category': 'letter'},
    'ص': {'english': 'sad', 'category': 'letter'},
    'ض': {'english': 'dad', 'category': 'letter'},
    'ط': {'english': 'ta', 'category': 'letter'},
    'ظ': {'english': 'dha', 'category': 'letter'},
    'ع': {'english': 'ain', 'category': 'letter'},
    'غ': {'english': 'ghain', 'category': 'letter'},
    'ف': {'english': 'fa', 'category': 'letter'},
    'ق': {'english': 'qaf', 'category': 'letter'},
    'ك': {'english': 'kaf', 'category': 'letter'},
    'ل': {'english': 'lam', 'category': 'letter'},
    'م': {'english': 'meem', 'category': 'letter'},
    'ن': {'english': 'noon', 'category': 'letter'},
    'ه': {'english': 'ha', 'category': 'letter'},
    'و': {'english': 'waw', 'category': 'letter'},
    'ي': {'english': 'ya', 'category': 'letter'},
}

# ============================================================================
# NUMBERS (0-9)
# ============================================================================

NUMBERS = {
    '0': {'arabic': '٠', 'english': 'zero', 'category': 'number'},
    '1': {'arabic': '١', 'english': 'one', 'category': 'number'},
    '2': {'arabic': '٢', 'english': 'two', 'category': 'number'},
    '3': {'arabic': '٣', 'english': 'three', 'category': 'number'},
    '4': {'arabic': '٤', 'english': 'four', 'category': 'number'},
    '5': {'arabic': '٥', 'english': 'five', 'category': 'number'},
    '6': {'arabic': '٦', 'english': 'six', 'category': 'number'},
    '7': {'arabic': '٧', 'english': 'seven', 'category': 'number'},
    '8': {'arabic': '٨', 'english': 'eight', 'category': 'number'},
    '9': {'arabic': '٩', 'english': 'nine', 'category': 'number'},
}

# ============================================================================
# ABSHER SERVICES VOCABULARY
# ============================================================================

ABSHER_SERVICES = {
    'استعلام': {'english': 'inquiry', 'category': 'service', 'intent': 'query'},
    'مخالفات': {'english': 'violations', 'category': 'service', 'intent': 'violations'},
    'مخالفة': {'english': 'violation', 'category': 'service', 'intent': 'violations'},
    'سيارة': {'english': 'car', 'category': 'service', 'intent': 'vehicle'},
    'لوحة': {'english': 'plate', 'category': 'service', 'intent': 'vehicle'},
    'رخصة': {'english': 'license', 'category': 'service', 'intent': 'license'},
    'قيادة': {'english': 'driving', 'category': 'service', 'intent': 'license'},
    'هوية': {'english': 'id', 'category': 'service', 'intent': 'identity'},
    'تجديد': {'english': 'renewal', 'category': 'service', 'intent': 'renewal'},
    'جواز': {'english': 'passport', 'category': 'service', 'intent': 'passport'},
    'سفر': {'english': 'travel', 'category': 'service', 'intent': 'travel'},
    'تأشيرة': {'english': 'visa', 'category': 'service', 'intent': 'visa'},
    'إقامة': {'english': 'residence', 'category': 'service', 'intent': 'residence'},
    'مقيم': {'english': 'resident', 'category': 'service', 'intent': 'residence'},
    'موعد': {'english': 'appointment', 'category': 'service', 'intent': 'appointment'},
    'حجز': {'english': 'booking', 'category': 'service', 'intent': 'booking'},
    'دفع': {'english': 'payment', 'category': 'service', 'intent': 'payment'},
    'سداد': {'english': 'pay', 'category': 'service', 'intent': 'payment'},
    'فاتورة': {'english': 'bill', 'category': 'service', 'intent': 'bill'},
    'غرامة': {'english': 'fine', 'category': 'service', 'intent': 'fine'},
    'شهادة': {'english': 'certificate', 'category': 'service', 'intent': 'certificate'},
    'ميلاد': {'english': 'birth', 'category': 'service', 'intent': 'birth'},
    'وفاة': {'english': 'death', 'category': 'service', 'intent': 'death'},
    'زواج': {'english': 'marriage', 'category': 'service', 'intent': 'marriage'},
    'طلاق': {'english': 'divorce', 'category': 'service', 'intent': 'divorce'},
    'عمل': {'english': 'work', 'category': 'service', 'intent': 'work'},
    'وظيفة': {'english': 'job', 'category': 'service', 'intent': 'job'},
    'تأمين': {'english': 'insurance', 'category': 'service', 'intent': 'insurance'},
    'صحي': {'english': 'health', 'category': 'service', 'intent': 'health'},
    'طبي': {'english': 'medical', 'category': 'service', 'intent': 'medical'},
    'مستشفى': {'english': 'hospital', 'category': 'service', 'intent': 'hospital'},
    'علاج': {'english': 'treatment', 'category': 'service', 'intent': 'treatment'},
}

# ============================================================================
# COMMON ACTION VERBS
# ============================================================================

ACTION_VERBS = {
    'أريد': {'english': 'I want', 'category': 'action', 'intent': 'request'},
    'أرغب': {'english': 'I wish', 'category': 'action', 'intent': 'request'},
    'أحتاج': {'english': 'I need', 'category': 'action', 'intent': 'request'},
    'اعرض': {'english': 'show', 'category': 'action', 'intent': 'display'},
    'افتح': {'english': 'open', 'category': 'action', 'intent': 'open'},
    'أغلق': {'english': 'close', 'category': 'action', 'intent': 'close'},
    'ابحث': {'english': 'search', 'category': 'action', 'intent': 'search'},
    'تحقق': {'english': 'check', 'category': 'action', 'intent': 'check'},
    'راجع': {'english': 'review', 'category': 'action', 'intent': 'review'},
    'طبع': {'english': 'print', 'category': 'action', 'intent': 'print'},
    'حمل': {'english': 'download', 'category': 'action', 'intent': 'download'},
    'أرسل': {'english': 'send', 'category': 'action', 'intent': 'send'},
    'احفظ': {'english': 'save', 'category': 'action', 'intent': 'save'},
    'احذف': {'english': 'delete', 'category': 'action', 'intent': 'delete'},
    'عدل': {'english': 'edit', 'category': 'action', 'intent': 'edit'},
    'أضف': {'english': 'add', 'category': 'action', 'intent': 'add'},
    'سجل': {'english': 'register', 'category': 'action', 'intent': 'register'},
    'دخول': {'english': 'login', 'category': 'action', 'intent': 'login'},
    'خروج': {'english': 'logout', 'category': 'action', 'intent': 'logout'},
    'رجوع': {'english': 'back', 'category': 'action', 'intent': 'back'},
    'التالي': {'english': 'next', 'category': 'action', 'intent': 'next'},
    'السابق': {'english': 'previous', 'category': 'action', 'intent': 'previous'},
    'موافق': {'english': 'ok', 'category': 'action', 'intent': 'confirm'},
    'إلغاء': {'english': 'cancel', 'category': 'action', 'intent': 'cancel'},
    'نعم': {'english': 'yes', 'category': 'action', 'intent': 'confirm'},
    'لا': {'english': 'no', 'category': 'action', 'intent': 'reject'},
}

# ============================================================================
# QUESTION WORDS
# ============================================================================

QUESTION_WORDS = {
    'ماذا': {'english': 'what', 'category': 'question'},
    'من': {'english': 'who', 'category': 'question'},
    'متى': {'english': 'when', 'category': 'question'},
    'أين': {'english': 'where', 'category': 'question'},
    'كيف': {'english': 'how', 'category': 'question'},
    'لماذا': {'english': 'why', 'category': 'question'},
    'كم': {'english': 'how many', 'category': 'question'},
    'أي': {'english': 'which', 'category': 'question'},
    'هل': {'english': 'is', 'category': 'question'},
}

# ============================================================================
# COMMON PHRASES (Pre-built for efficiency)
# ============================================================================

COMMON_PHRASES = {
    'صباح_الخير': {'text': 'صباح الخير', 'english': 'good morning', 'category': 'greeting'},
    'مساء_الخير': {'text': 'مساء الخير', 'english': 'good evening', 'category': 'greeting'},
    'السلام_عليكم': {'text': 'السلام عليكم', 'english': 'peace be upon you', 'category': 'greeting'},
    'شكرا': {'text': 'شكرا', 'english': 'thank you', 'category': 'courtesy'},
    'من_فضلك': {'text': 'من فضلك', 'english': 'please', 'category': 'courtesy'},
    'عفوا': {'text': 'عفوا', 'english': 'excuse me', 'category': 'courtesy'},
    'آسف': {'text': 'آسف', 'english': 'sorry', 'category': 'courtesy'},
    'مع_السلامة': {'text': 'مع السلامة', 'english': 'goodbye', 'category': 'farewell'},
    
    # Service-specific phrases
    'استعلام_عن_المخالفات': {
        'text': 'استعلام عن المخالفات',
        'english': 'violations inquiry',
        'category': 'service_phrase',
        'intent': 'violations_inquiry'
    },
    'تجديد_الهوية': {
        'text': 'تجديد الهوية',
        'english': 'id renewal',
        'category': 'service_phrase',
        'intent': 'id_renewal'
    },
    'تجديد_رخصة_القيادة': {
        'text': 'تجديد رخصة القيادة',
        'english': 'driving license renewal',
        'category': 'service_phrase',
        'intent': 'license_renewal'
    },
    'استخراج_جواز_سفر': {
        'text': 'استخراج جواز سفر',
        'english': 'passport issuance',
        'category': 'service_phrase',
        'intent': 'passport_issuance'
    },
}

# ============================================================================
# COMPLETE VOCABULARY (Combined)
# ============================================================================

COMPLETE_VOCABULARY = {
    **ARABIC_LETTERS,
    **{f'num_{k}': v for k, v in NUMBERS.items()},
    **ABSHER_SERVICES,
    **ACTION_VERBS,
    **QUESTION_WORDS,
    **COMMON_PHRASES,
}

# ============================================================================
# INTENT TO SERVICE MAPPING (For Navigation)
# ============================================================================

INTENT_TO_SERVICE = {
    'violations_inquiry': {
        'url': '/violations/',
        'service_name': 'الاستعلام عن المخالفات',
        'service_name_en': 'Violations Inquiry',
        'actions': ['query_violations', 'pay_fine']
    },
    'id_renewal': {
        'url': '/id-renewal/',
        'service_name': 'تجديد الهوية',
        'service_name_en': 'ID Renewal',
        'actions': ['renew_id', 'upload_documents']
    },
    'license_renewal': {
        'url': '/license-renewal/',
        'service_name': 'تجديد رخصة القيادة',
        'service_name_en': 'License Renewal',
        'actions': ['renew_license', 'medical_test']
    },
    'passport_issuance': {
        'url': '/passport/',
        'service_name': 'استخراج جواز السفر',
        'service_name_en': 'Passport Issuance',
        'actions': ['apply_passport', 'track_application']
    },
    'absher_individuals': {
        'url': '/absher-individuals/',
        'service_name': 'أبشر أفراد',
        'service_name_en': 'Absher Individuals',
        'actions': ['view_profile', 'services_menu']
    },
    'profile': {
        'url': '/profile-setup/',
        'service_name': 'الملف الشخصي',
        'service_name_en': 'Profile',
        'actions': ['view_profile', 'edit_profile']
    },
    'services': {
        'url': '/services/',
        'service_name': 'الخدمات',
        'service_name_en': 'Services',
        'actions': ['browse_services']
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_word_info(word: str) -> dict:
    """Get information about a word from vocabulary."""
    return COMPLETE_VOCABULARY.get(word, None)

def get_intent_from_text(text: str) -> str:
    """Extract intent from Arabic text using keyword matching."""
    text_lower = text.lower().strip()
    
    # Check for direct phrase match first
    for phrase_key, phrase_data in COMMON_PHRASES.items():
        if phrase_data.get('text', '').lower() in text_lower:
            return phrase_data.get('intent', 'unknown')
    
    # Check for service keywords
    intents_found = []
    for word, data in ABSHER_SERVICES.items():
        if word in text_lower:
            intents_found.append(data.get('intent', ''))
    
    # Check for action verbs
    for word, data in ACTION_VERBS.items():
        if word in text_lower:
            intents_found.append(data.get('intent', ''))
    
    # Determine primary intent
    if 'violations' in intents_found or 'مخالفات' in text_lower:
        return 'violations_inquiry'
    elif 'identity' in intents_found or 'هوية' in text_lower:
        if 'renewal' in intents_found or 'تجديد' in text_lower:
            return 'id_renewal'
    elif 'license' in intents_found or 'رخصة' in text_lower:
        return 'license_renewal'
    elif 'passport' in intents_found or 'جواز' in text_lower:
        return 'passport_issuance'
    elif 'profile' in intents_found or 'ملف' in text_lower:
        return 'profile'
    
    return 'services'  # Default to services page

def get_service_from_intent(intent: str) -> dict:
    """Get service information from intent."""
    return INTENT_TO_SERVICE.get(intent, INTENT_TO_SERVICE['services'])

def text_to_keywords(text: str) -> list:
    """Convert text to list of keywords for processing."""
    words = text.split()
    keywords = []
    
    for word in words:
        word_info = get_word_info(word)
        if word_info:
            keywords.append({
                'word': word,
                'english': word_info.get('english', ''),
                'category': word_info.get('category', ''),
                'intent': word_info.get('intent', '')
            })
    
    return keywords

