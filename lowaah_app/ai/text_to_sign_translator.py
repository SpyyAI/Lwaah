"""
Text-to-Sign Language Translator
Converts Arabic/English text into sign language representation.

Output formats:
1. 3D Avatar animation data (JSON format for WebGL/Three.js)
2. Sign sequence description (for avatar rendering)
3. Video references (pre-recorded signs)
"""

import json
from typing import List, Dict, Optional, Tuple
import re


class TextToSignTranslator:
    """
    Translates text to sign language representation.
    Outputs animation data for 3D avatar rendering.
    """
    
    def __init__(self):
        """Initialize translator with vocabulary."""
        from .sign_language_vocabulary import (
            ARABIC_LETTERS,
            NUMBERS,
            ABSHER_SERVICES,
            ACTION_VERBS,
            QUESTION_WORDS,
            COMMON_PHRASES
        )
        
        self.letters = ARABIC_LETTERS
        self.numbers = NUMBERS
        self.services = ABSHER_SERVICES
        self.actions = ACTION_VERBS
        self.questions = QUESTION_WORDS
        self.phrases = COMMON_PHRASES
        
        # Build complete sign database
        self.sign_database = self._build_sign_database()
        
        print("✅ TextToSignTranslator initialized")
    
    def _build_sign_database(self) -> Dict:
        """
        Build comprehensive sign database with animation data.
        Each sign maps to animation keyframes for 3D avatar.
        """
        database = {}
        
        # Add letters (finger spelling)
        for letter, info in self.letters.items():
            database[letter] = {
                'type': 'letter',
                'character': letter,
                'english': info['english'],
                'animation': self._get_letter_animation(letter),
                'duration': 0.8,  # seconds
                'hand_shape': self._get_hand_shape_for_letter(letter)
            }
        
        # Add numbers
        for num, info in self.numbers.items():
            database[num] = {
                'type': 'number',
                'value': num,
                'arabic': info['arabic'],
                'animation': self._get_number_animation(num),
                'duration': 0.8,
                'hand_shape': self._get_hand_shape_for_number(num)
            }
        
        # Add words (services, actions, etc.)
        for word_dict in [self.services, self.actions, self.questions]:
            for word, info in word_dict.items():
                database[word] = {
                    'type': 'word',
                    'text': word,
                    'english': info['english'],
                    'animation': self._get_word_animation(word),
                    'duration': 1.2,
                    'category': info['category']
                }
        
        # Add phrases (compound signs)
        for phrase_key, info in self.phrases.items():
            text = info['text']
            database[text] = {
                'type': 'phrase',
                'text': text,
                'english': info['english'],
                'animation': self._get_phrase_animation(text),
                'duration': 2.0,
                'category': info['category']
            }
        
        return database
    
    def translate(self, text: str) -> Dict:
        """
        Translate text to sign language animation sequence.
        
        Args:
            text: Input text (Arabic or English)
            
        Returns:
            Dictionary with sign sequence and animation data
        """
        if not text or len(text.strip()) == 0:
            return {
                'success': False,
                'error': 'Empty text',
                'signs': []
            }
        
        text_clean = text.strip()
        
        # Step 1: Check if entire text is a known phrase
        if text_clean in self.sign_database:
            sign_data = self.sign_database[text_clean]
            return {
                'success': True,
                'text': text_clean,
                'signs': [sign_data],
                'total_duration': sign_data['duration'],
                'translation_type': 'phrase'
            }
        
        # Step 2: Word-by-word translation
        words = text_clean.split()
        sign_sequence = []
        total_duration = 0.0
        
        for word in words:
            word_clean = word.strip()
            
            # Try direct word match
            if word_clean in self.sign_database:
                sign_data = self.sign_database[word_clean]
                sign_sequence.append(sign_data)
                total_duration += sign_data['duration']
            else:
                # Fallback: Finger spelling (character by character)
                for char in word_clean:
                    if char in self.sign_database:
                        char_sign = self.sign_database[char]
                        sign_sequence.append(char_sign)
                        total_duration += char_sign['duration']
                    elif char == ' ':
                        # Add pause for space
                        sign_sequence.append({
                            'type': 'pause',
                            'duration': 0.3
                        })
                        total_duration += 0.3
        
        return {
            'success': True,
            'text': text_clean,
            'signs': sign_sequence,
            'total_duration': total_duration,
            'translation_type': 'word_by_word'
        }
    
    def _get_letter_animation(self, letter: str) -> Dict:
        """
        Get animation data for a letter sign.
        Returns hand pose keyframes for 3D avatar.
        """
        # This would contain actual hand joint rotations/positions
        # For now, returning placeholder structure
        return {
            'keyframes': [
                {
                    'time': 0.0,
                    'hand': 'right',
                    'pose': self._get_hand_shape_for_letter(letter),
                    'position': [0, 1.2, 0.3],  # x, y, z in front of body
                    'rotation': [0, 0, 0]  # euler angles
                }
            ]
        }
    
    def _get_number_animation(self, number: str) -> Dict:
        """Get animation data for a number sign."""
        return {
            'keyframes': [
                {
                    'time': 0.0,
                    'hand': 'right',
                    'pose': self._get_hand_shape_for_number(number),
                    'position': [0, 1.2, 0.3],
                    'rotation': [0, 0, 0]
                }
            ]
        }
    
    def _get_word_animation(self, word: str) -> Dict:
        """Get animation data for a word sign."""
        # Words typically have motion paths
        return {
            'keyframes': [
                {
                    'time': 0.0,
                    'hand': 'right',
                    'pose': self._get_hand_shape_for_word(word),
                    'position': [0, 1.2, 0.3],
                    'rotation': [0, 0, 0]
                },
                {
                    'time': 0.6,
                    'hand': 'right',
                    'pose': self._get_hand_shape_for_word(word),
                    'position': [0.2, 1.2, 0.3],
                    'rotation': [0, 10, 0]
                }
            ]
        }
    
    def _get_phrase_animation(self, phrase: str) -> Dict:
        """Get animation data for a phrase sign."""
        return {
            'keyframes': [
                {
                    'time': 0.0,
                    'hand': 'right',
                    'pose': 'open_hand',
                    'position': [0, 1.2, 0.3],
                    'rotation': [0, 0, 0]
                },
                {
                    'time': 1.0,
                    'hand': 'right',
                    'pose': 'pointing',
                    'position': [0.3, 1.1, 0.4],
                    'rotation': [0, 15, 0]
                }
            ]
        }
    
    def _get_hand_shape_for_letter(self, letter: str) -> str:
        """
        Get hand shape identifier for Arabic letter.
        Maps to predefined hand poses in 3D avatar.
        """
        # Simplified mapping (expand with actual KSL alphabet)
        letter_shapes = {
            'أ': 'fist_with_thumb_up',
            'ب': 'flat_hand_vertical',
            'ت': 'three_fingers',
            'ث': 'three_fingers_spread',
            'ج': 'curved_hand',
            'ح': 'c_shape',
            'خ': 'c_shape_rotated',
            'د': 'pointing_up',
            'ذ': 'pointing_up_thumb',
            'ر': 'two_fingers_crossed',
            'ز': 'two_fingers_crossed_shake',
            'س': 'three_fingers_together',
            'ش': 'three_fingers_spread',
            'ص': 's_shape',
            'ض': 's_shape_rotated',
            'ط': 't_shape',
            'ظ': 't_shape_thumb',
            'ع': 'o_shape',
            'غ': 'o_shape_shake',
            'ف': 'f_shape',
            'ق': 'q_shape',
            'ك': 'k_shape',
            'ل': 'l_shape',
            'م': 'm_shape',
            'ن': 'n_shape',
            'ه': 'h_shape',
            'و': 'w_shape',
            'ي': 'y_shape',
        }
        
        return letter_shapes.get(letter, 'flat_hand')
    
    def _get_hand_shape_for_number(self, number: str) -> str:
        """Get hand shape for number."""
        number_shapes = {
            '0': 'o_shape',
            '1': 'one_finger',
            '2': 'two_fingers',
            '3': 'three_fingers',
            '4': 'four_fingers',
            '5': 'five_fingers',
            '6': 'thumb_pinky',
            '7': 'thumb_ring_pinky',
            '8': 'thumb_middle_ring_pinky',
            '9': 'all_except_index',
        }
        
        return number_shapes.get(number, 'flat_hand')
    
    def _get_hand_shape_for_word(self, word: str) -> str:
        """Get hand shape for word sign."""
        # Context-dependent hand shapes
        if 'استعلام' in word or 'بحث' in word:
            return 'pointing_forward'
        elif 'تجديد' in word:
            return 'rotating_hands'
        elif 'دفع' in word or 'سداد' in word:
            return 'flat_hand_forward'
        else:
            return 'neutral_hand'
    
    def export_for_avatar(self, translation: Dict) -> str:
        """
        Export translation in format ready for 3D avatar.
        Returns JSON string for WebGL/Three.js consumption.
        
        Args:
            translation: Output from translate() method
            
        Returns:
            JSON string with animation timeline
        """
        if not translation['success']:
            return json.dumps({'error': translation.get('error')})
        
        avatar_data = {
            'version': '1.0',
            'text': translation['text'],
            'total_duration': translation['total_duration'],
            'signs': []
        }
        
        current_time = 0.0
        
        for sign in translation['signs']:
            sign_export = {
                'start_time': current_time,
                'end_time': current_time + sign.get('duration', 1.0),
                'type': sign.get('type'),
                'animation': sign.get('animation'),
            }
            
            # Add text info for display
            if sign['type'] == 'letter':
                sign_export['display_text'] = sign.get('character', '')
            elif sign['type'] in ['word', 'phrase']:
                sign_export['display_text'] = sign.get('text', '')
            elif sign['type'] == 'number':
                sign_export['display_text'] = sign.get('value', '')
            
            avatar_data['signs'].append(sign_export)
            current_time += sign.get('duration', 1.0)
        
        return json.dumps(avatar_data, ensure_ascii=False, indent=2)
    
    def get_video_references(self, translation: Dict) -> List[str]:
        """
        Get video file references for pre-recorded signs.
        Useful as fallback when 3D avatar is not available.
        
        Args:
            translation: Output from translate() method
            
        Returns:
            List of video file paths
        """
        videos = []
        
        for sign in translation['signs']:
            if sign['type'] == 'letter':
                video_path = f"/static/signs/letters/{sign['character']}.mp4"
                videos.append(video_path)
            elif sign['type'] == 'word':
                # Sanitize word for filename
                word_safe = re.sub(r'[^\w\s-]', '', sign['text'])
                video_path = f"/static/signs/words/{word_safe}.mp4"
                videos.append(video_path)
            elif sign['type'] == 'phrase':
                phrase_safe = re.sub(r'[^\w\s-]', '', sign['text'])
                video_path = f"/static/signs/phrases/{phrase_safe}.mp4"
                videos.append(video_path)
        
        return videos
    
    def create_subtitles(self, translation: Dict) -> str:
        """
        Create subtitle track (SRT format) for sign videos.
        
        Args:
            translation: Output from translate() method
            
        Returns:
            SRT formatted subtitle string
        """
        if not translation['success']:
            return ""
        
        srt_content = []
        current_time = 0.0
        
        for idx, sign in enumerate(translation['signs'], 1):
            duration = sign.get('duration', 1.0)
            end_time = current_time + duration
            
            # Format timestamps
            start_ts = self._format_srt_time(current_time)
            end_ts = self._format_srt_time(end_time)
            
            # Get display text
            if sign['type'] == 'letter':
                text = sign.get('character', '')
            elif sign['type'] in ['word', 'phrase']:
                text = sign.get('text', '')
            elif sign['type'] == 'number':
                text = sign.get('value', '')
            else:
                text = ''
            
            # Build SRT entry
            srt_entry = f"{idx}\n{start_ts} --> {end_ts}\n{text}\n"
            srt_content.append(srt_entry)
            
            current_time = end_time
        
        return "\n".join(srt_content)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format time in SRT format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ============================================================================
# TESTING
# ============================================================================

def test_translator():
    """Test text-to-sign translator."""
    translator = TextToSignTranslator()
    
    test_texts = [
        "استعلام عن المخالفات",
        "تجديد الهوية",
        "أريد الاستعلام",
        "صباح الخير",
        "١٢٣٤",
    ]
    
    print("\n" + "="*60)
    print("Testing Text-to-Sign Translator")
    print("="*60)
    
    for text in test_texts:
        print(f"\n📝 Text: {text}")
        translation = translator.translate(text)
        
        if translation['success']:
            print(f"   ✅ Success!")
            print(f"   Signs: {len(translation['signs'])}")
            print(f"   Duration: {translation['total_duration']:.1f}s")
            print(f"   Type: {translation['translation_type']}")
            
            # Show avatar export
            avatar_json = translator.export_for_avatar(translation)
            print(f"   Avatar data: {len(avatar_json)} chars")
        else:
            print(f"   ❌ Error: {translation['error']}")


if __name__ == "__main__":
    test_translator()


