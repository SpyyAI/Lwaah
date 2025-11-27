"""
Wake Word Detection System
Detects "أبشر" (Absher) wake word in Arabic speech
"""

import re
from typing import Tuple, Optional


class WakeWordDetector:
    """Detects wake words in speech input"""
    
    def __init__(self):
        # Wake words and variations
        self.wake_words = [
            'أبشر', 'ابشر', 'ابشر', 'أبشر',
            'absher', 'ابشار', 'ابشار'
        ]
        
        # Confidence threshold
        self.confidence_threshold = 0.7
        
    def detect(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Detect wake word in text
        
        Returns:
            (detected, remaining_text)
        """
        # Normalize text
        text = text.strip().lower()
        
        # Normalize Arabic
        text = self._normalize_arabic(text)
        
        # Check for wake word
        for wake_word in self.wake_words:
            normalized_wake = self._normalize_arabic(wake_word.lower())
            
            if normalized_wake in text:
                # Found wake word
                # Remove it and return remaining text
                remaining = text.replace(normalized_wake, '').strip()
                return True, remaining if remaining else None
                
        return False, None
        
    def is_wake_word_only(self, text: str) -> bool:
        """Check if text is ONLY the wake word"""
        text = text.strip().lower()
        text = self._normalize_arabic(text)
        
        return any(text == self._normalize_arabic(wake.lower()) 
                  for wake in self.wake_words)
        
    def extract_command_after_wake_word(self, text: str) -> Optional[str]:
        """
        Extract command that comes after wake word
        
        Example: "أبشر تجديد الهوية" -> "تجديد الهوية"
        """
        detected, remaining = self.detect(text)
        if detected and remaining and len(remaining) > 2:
            return remaining
        return None
        
    def _normalize_arabic(self, text: str) -> str:
        """Normalize Arabic text for comparison"""
        replacements = {
            'أ': 'ا',
            'إ': 'ا',
            'آ': 'ا',
            'ٱ': 'ا',
            'ة': 'ه',
            'ى': 'ي',
            'ئ': 'ي',
            'ؤ': 'و',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # Remove diacritics
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        
        return text
        
    def get_confidence(self, text: str) -> float:
        """
        Get confidence score for wake word detection
        
        Returns value between 0.0 and 1.0
        """
        text = text.strip().lower()
        text = self._normalize_arabic(text)
        
        best_score = 0.0
        
        for wake_word in self.wake_words:
            normalized_wake = self._normalize_arabic(wake_word.lower())
            
            # Exact match
            if normalized_wake == text:
                return 1.0
                
            # Contains wake word
            if normalized_wake in text:
                # Calculate score based on position and surrounding words
                words = text.split()
                if normalized_wake in words:
                    # Wake word as separate word
                    best_score = max(best_score, 0.95)
                else:
                    # Wake word as substring
                    best_score = max(best_score, 0.8)
                    
            # Fuzzy match (Levenshtein-like)
            similarity = self._string_similarity(normalized_wake, text)
            best_score = max(best_score, similarity)
            
        return best_score
        
    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings"""
        if not s1 or not s2:
            return 0.0
            
        # Simple character overlap ratio
        s1_chars = set(s1)
        s2_chars = set(s2)
        
        intersection = s1_chars.intersection(s2_chars)
        union = s1_chars.union(s2_chars)
        
        if not union:
            return 0.0
            
        return len(intersection) / len(union)


# Global wake word detector instance
wake_word_detector = WakeWordDetector()

