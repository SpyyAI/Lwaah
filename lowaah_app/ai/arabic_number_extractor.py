"""
Arabic Number Extractor
Handles both Arabic and English spoken numbers
"""

import re
from typing import Optional


class ArabicNumberExtractor:
    """Extract numbers from Arabic speech"""
    
    def __init__(self):
        # Arabic digit words
        self.arabic_digits = {
            'صفر': '0', 'سفر': '0',
            'واحد': '1', 'واحده': '1', 'وحد': '1',
            'اثنين': '2', 'اثنان': '2', 'ثنين': '2', 'اتنين': '2',
            'ثلاثة': '3', 'ثلاث': '3', 'تلاته': '3', 'تلاتة': '3',
            'اربعة': '4', 'اربع': '4', 'أربعة': '4', 'أربع': '4', 'اربعه': '4',
            'خمسة': '5', 'خمس': '5', 'خمسه': '5',
            'ستة': '6', 'ست': '6', 'سته': '6', 'سيته': '6',
            'سبعة': '7', 'سبع': '7', 'سبعه': '7',
            'ثمانية': '8', 'ثماني': '8', 'ثمانيه': '8', 'تمانية': '8', 'تماني': '8',
            'تسعة': '9', 'تسع': '9', 'تسعه': '9',
        }
        
        # English digit words
        self.english_digits = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
        }
        
    def extract_saudi_id(self, text: str) -> Optional[str]:
        """Extract Saudi ID number (10 digits) from text"""
        
        # Try direct digit extraction first
        id_number = self.extract_digits(text)
        
        if id_number and len(id_number) == 10:
            return id_number
        
        # Try word-based extraction
        id_number = self.extract_from_words(text)
        
        if id_number and len(id_number) == 10:
            return id_number
            
        return None
        
    def extract_digits(self, text: str) -> str:
        """Extract all digits from text (Arabic and English numerals)"""
        
        # Convert Arabic numerals to English
        arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        text = text.translate(arabic_to_english)
        
        # Extract only digits
        digits = ''.join(c for c in text if c.isdigit())
        
        return digits
        
    def extract_from_words(self, text: str) -> str:
        """Extract digits from spoken words"""
        
        text = text.lower().strip()
        result = []
        
        # Split by spaces and common separators
        words = re.split(r'[\s,،.و]+', text)
        
        for word in words:
            word = word.strip()
            
            # Check Arabic digits
            if word in self.arabic_digits:
                result.append(self.arabic_digits[word])
            # Check English digits
            elif word in self.english_digits:
                result.append(self.english_digits[word])
            # Check if it's a digit character
            elif word.isdigit():
                result.append(word)
                
        return ''.join(result)
        
    def validate_saudi_id(self, id_number: str) -> bool:
        """Validate Saudi national ID format"""
        
        if not id_number or len(id_number) != 10:
            return False
            
        if not id_number.isdigit():
            return False
            
        # First digit must be 1 or 2 (Saudi nationals)
        if id_number[0] not in ['1', '2']:
            return False
            
        return True
        
    def extract_plate_number(self, text: str) -> Optional[str]:
        """Extract vehicle plate number"""
        
        # Try to extract alphanumeric plate
        text = text.upper()
        
        # Common patterns: ABC1234, 1234ABC, etc.
        patterns = [
            r'([A-Z]{3}\s*\d{4})',
            r'(\d{4}\s*[A-Z]{3})',
            r'([A-Z]{3}\d{4})',
            r'(\d{4}[A-Z]{3})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                plate = match.group(1).replace(' ', '')
                return plate
                
        # Fallback: just extract what we can
        return self.extract_digits(text)
        
    def format_id_for_display(self, id_number: str) -> str:
        """Format ID number for display with spaces"""
        if len(id_number) == 10:
            # Format as: XXX XXX XXXX
            return f"{id_number[:3]} {id_number[3:6]} {id_number[6:]}"
        return id_number


# Global instance
arabic_number_extractor = ArabicNumberExtractor()

