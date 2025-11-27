"""
Page-Aware Conversational Workflows
Handles form filling on specific pages through voice
"""

from typing import Dict, Any, Optional, List
from .arabic_number_extractor import arabic_number_extractor


class PageAwareWorkflow:
    """Base class for page-specific workflows"""
    
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.current_field = None
        self.form_data = {}
        self.field_order = []
        self.current_index = 0
        
    def get_next_field(self) -> Optional[Dict[str, Any]]:
        """Get next field to fill"""
        if self.current_index < len(self.field_order):
            field = self.field_order[self.current_index]
            self.current_field = field
            return field
        return None
        
    def set_field_value(self, field_name: str, value: str):
        """Set field value"""
        self.form_data[field_name] = value
        
    def move_to_next_field(self):
        """Move to next field"""
        self.current_index += 1
        
    def is_complete(self) -> bool:
        """Check if all fields are filled"""
        return self.current_index >= len(self.field_order)
        
    def reset(self):
        """Reset workflow"""
        self.current_field = None
        self.form_data = {}
        self.current_index = 0


class ViolationsPageWorkflow(PageAwareWorkflow):
    """Violations page form filling workflow"""
    
    def __init__(self):
        super().__init__('violations')
        
        # Define form fields in order (using actual HTML field IDs)
        self.field_order = [
            {
                'name': 'idNumber',  # Actual HTML field ID (camelCase)
                'backend_name': 'id_number',  # For processing
                'type': 'number',
                'prompt_ar': 'قل رقم الهوية من فضلك',
                'prompt_en': 'Please say your ID number',
                'validation': lambda x: len(x) == 10 and x.isdigit(),
                'error_ar': 'رقم الهوية يجب أن يكون 10 أرقام',
                'error_en': 'ID must be 10 digits'
            },
            {
                'name': 'plateNumber',  # Actual HTML field ID
                'backend_name': 'plate_number',
                'type': 'text',
                'prompt_ar': 'قل رقم اللوحة من فضلك',
                'prompt_en': 'Please say the plate number',
                'validation': lambda x: len(x) >= 3,
                'error_ar': 'رقم اللوحة غير صحيح',
                'error_en': 'Invalid plate number'
            },
            {
                'name': 'confirm',
                'backend_name': 'confirm',
                'type': 'confirmation',
                'prompt_ar': 'هل تريد البحث الآن؟ قل نعم أو لا',
                'prompt_en': 'Search now? Say yes or no',
                'validation': None,
                'error_ar': None,
                'error_en': None
            }
        ]


class IDRenewalPageWorkflow(PageAwareWorkflow):
    """ID Renewal page form filling workflow"""
    
    def __init__(self):
        super().__init__('id_renewal')
        
        self.field_order = [
            {
                'name': 'id_number',
                'type': 'number',
                'prompt_ar': 'قل رقم الهوية الوطنية',
                'prompt_en': 'Say your national ID number',
                'validation': lambda x: len(x) == 10 and x.isdigit(),
                'error_ar': 'رقم الهوية يجب أن يكون 10 أرقام',
                'error_en': 'ID must be 10 digits'
            },
            {
                'name': 'use_camera',
                'type': 'confirmation',
                'prompt_ar': 'هل تريد استخدام الكاميرا لتصوير الهوية؟ قل نعم أو لا',
                'prompt_en': 'Use camera to scan ID? Say yes or no',
                'validation': None,
                'error_ar': None,
                'error_en': None
            }
        ]


class PassportPageWorkflow(PageAwareWorkflow):
    """Passport page form filling workflow"""
    
    def __init__(self):
        super().__init__('passport')
        
        self.field_order = [
            {
                'name': 'service_type',
                'type': 'choice',
                'prompt_ar': 'ما نوع الخدمة؟ قل: جديد، تجديد، أو استعلام',
                'prompt_en': 'Service type? Say: new, renewal, or inquiry',
                'choices': ['جديد', 'new', 'تجديد', 'renewal', 'استعلام', 'inquiry'],
                'validation': None,
                'error_ar': 'قل: جديد، تجديد، أو استعلام',
                'error_en': 'Say: new, renewal, or inquiry'
            },
            {
                'name': 'id_number',
                'type': 'number',
                'prompt_ar': 'قل رقم الهوية',
                'prompt_en': 'Say your ID number',
                'validation': lambda x: len(x) == 10 and x.isdigit(),
                'error_ar': 'رقم الهوية يجب أن يكون 10 أرقام',
                'error_en': 'ID must be 10 digits'
            },
            {
                'name': 'confirm',
                'type': 'confirmation',
                'prompt_ar': 'هل المعلومات صحيحة؟ قل نعم أو لا',
                'prompt_en': 'Is the information correct? Say yes or no',
                'validation': None,
                'error_ar': None,
                'error_en': None
            }
        ]


class DrivingLicensePageWorkflow(PageAwareWorkflow):
    """Driving License page form filling workflow"""
    
    def __init__(self):
        super().__init__('driving_license')
        
        self.field_order = [
            {
                'name': 'service_type',
                'type': 'choice',
                'prompt_ar': 'ما الخدمة المطلوبة؟ قل: إصدار، تجديد، أو استعلام',
                'prompt_en': 'What service? Say: issue, renewal, or inquiry',
                'choices': ['إصدار', 'issue', 'تجديد', 'renewal', 'استعلام', 'inquiry'],
                'validation': None,
                'error_ar': 'قل: إصدار، تجديد، أو استعلام',
                'error_en': 'Say: issue, renewal, or inquiry'
            },
            {
                'name': 'id_number',
                'type': 'number',
                'prompt_ar': 'قل رقم الهوية',
                'prompt_en': 'Say your ID number',
                'validation': lambda x: len(x) == 10 and x.isdigit(),
                'error_ar': 'رقم الهوية غير صحيح',
                'error_en': 'Invalid ID number'
            }
        ]


class VehicleRegistrationPageWorkflow(PageAwareWorkflow):
    """Vehicle Registration page form filling workflow"""
    
    def __init__(self):
        super().__init__('vehicle_registration')
        
        self.field_order = [
            {
                'name': 'plate_number',
                'type': 'text',
                'prompt_ar': 'قل رقم اللوحة',
                'prompt_en': 'Say the plate number',
                'validation': lambda x: len(x) >= 3,
                'error_ar': 'رقم اللوحة غير صحيح',
                'error_en': 'Invalid plate number'
            },
            {
                'name': 'owner_id',
                'type': 'number',
                'prompt_ar': 'قل رقم هوية المالك',
                'prompt_en': 'Say owner ID number',
                'validation': lambda x: len(x) == 10 and x.isdigit(),
                'error_ar': 'رقم الهوية يجب أن يكون 10 أرقام',
                'error_en': 'ID must be 10 digits'
            }
        ]


class WorkflowFactory:
    """Factory to create page-specific workflows"""
    
    @staticmethod
    def create_workflow(page_name: str) -> Optional[PageAwareWorkflow]:
        """Create workflow for specific page"""
        workflows = {
            'violations': ViolationsPageWorkflow,
            'id_renewal': IDRenewalPageWorkflow,
            'passport': PassportPageWorkflow,
            'driving_license': DrivingLicensePageWorkflow,
            'vehicle_registration': VehicleRegistrationPageWorkflow,
        }
        
        workflow_class = workflows.get(page_name)
        if workflow_class:
            return workflow_class()
        return None


class PageAwareConversationManager:
    """Manages page-aware conversations"""
    
    def __init__(self):
        self.current_workflow = None
        self.current_page = None
        self.in_form_filling = False
        
    def start_page_workflow(self, page_name: str) -> Optional[Dict[str, Any]]:
        """Start workflow for a specific page"""
        self.current_workflow = WorkflowFactory.create_workflow(page_name)
        self.current_page = page_name
        self.in_form_filling = True
        
        if self.current_workflow:
            # Get first field
            field = self.current_workflow.get_next_field()
            if field:
                return {
                    'arabic': field['prompt_ar'],
                    'english': field['prompt_en'],
                    'field': field['name'],
                    'action': None,
                    'continue_conversation': True
                }
        
        return None
        
    def process_field_input(self, user_input: str) -> Dict[str, Any]:
        """Process input for current field"""
        
        # SILENCE DETECTION: Check if input is empty
        if not user_input or len(user_input.strip()) < 2:
            return {
                'arabic': 'لم أسمع إجابة. هل تكرر من فضلك؟',
                'english': 'I did not hear an answer. Could you repeat please?',
                'action': None,
                'continue_conversation': True,
                'silence_detected': True
            }
        
        if not self.current_workflow or not self.current_workflow.current_field:
            return {
                'arabic': 'خطأ في النظام',
                'english': 'System error',
                'action': None,
                'continue_conversation': False
            }
            
        current_field = self.current_workflow.current_field
        field_name = current_field['name']
        field_type = current_field['type']
        
        # Process based on field type
        if field_type == 'number':
            # Extract numbers using advanced extractor
            if field_name == 'id_number':
                value = arabic_number_extractor.extract_saudi_id(user_input)
                
                # Validate Saudi ID
                if not value or not arabic_number_extractor.validate_saudi_id(value):
                    return {
                        'arabic': 'رقم الهوية غير صحيح. يجب أن يكون 10 أرقام. حاول مرة أخرى',
                        'english': 'Invalid ID. Must be 10 digits. Try again',
                        'field': field_name,
                        'action': None,
                        'continue_conversation': True,
                        'retry': True
                    }
            else:
                # General number extraction
                value = arabic_number_extractor.extract_digits(user_input)
                
                # Validate if validator exists
                if current_field['validation'] and not current_field['validation'](value):
                    return {
                        'arabic': current_field['error_ar'],
                        'english': current_field['error_en'],
                        'field': field_name,
                        'action': None,
                        'continue_conversation': True,
                        'retry': True
                    }
            
            # Store value
            self.current_workflow.set_field_value(field_name, value)
            
            # Move to next field
            self.current_workflow.move_to_next_field()
            
            # Check if more fields
            if self.current_workflow.is_complete():
                return self._complete_form()
            else:
                next_field = self.current_workflow.get_next_field()
                
                # Format ID for confirmation
                formatted_value = value
                if field_name == 'id_number':
                    formatted_value = arabic_number_extractor.format_id_for_display(value)
                
                return {
                    'arabic': f'تم إدخال {formatted_value}. {next_field["prompt_ar"]}',
                    'english': f'Entered {formatted_value}. {next_field["prompt_en"]}',
                    'field': next_field['name'],
                    'action': {
                        'type': 'fill_field',
                        'field': field_name,
                        'value': value
                    },
                    'continue_conversation': True
                }
                
        elif field_type == 'confirmation':
            if self._is_affirmative(user_input):
                return self._complete_form()
            else:
                return {
                    'arabic': 'تم الإلغاء. قل "أبشر" للبدء من جديد',
                    'english': 'Cancelled. Say "Absher" to start again',
                    'action': None,
                    'continue_conversation': False
                }
                
        elif field_type == 'text':
            # Store text value
            value = user_input.strip()
            
            if current_field['validation'] and not current_field['validation'](value):
                return {
                    'arabic': current_field['error_ar'],
                    'english': current_field['error_en'],
                    'field': field_name,
                    'action': None,
                    'continue_conversation': True,
                    'retry': True
                }
            
            self.current_workflow.set_field_value(field_name, value)
            self.current_workflow.move_to_next_field()
            
            if self.current_workflow.is_complete():
                return self._complete_form()
            else:
                next_field = self.current_workflow.get_next_field()
                return {
                    'arabic': next_field['prompt_ar'],
                    'english': next_field['prompt_en'],
                    'field': next_field['name'],
                    'action': {
                        'type': 'fill_field',
                        'field': field_name,
                        'value': value
                    },
                    'continue_conversation': True
                }
                
        elif field_type == 'choice':
            # Check if input matches any choice
            normalized_input = self._normalize_arabic(user_input.lower())
            
            matched = False
            for choice in current_field['choices']:
                if self._normalize_arabic(choice.lower()) in normalized_input:
                    self.current_workflow.set_field_value(field_name, choice)
                    matched = True
                    break
            
            if not matched:
                return {
                    'arabic': current_field['error_ar'],
                    'english': current_field['error_en'],
                    'field': field_name,
                    'action': None,
                    'continue_conversation': True,
                    'retry': True
                }
            
            self.current_workflow.move_to_next_field()
            
            if self.current_workflow.is_complete():
                return self._complete_form()
            else:
                next_field = self.current_workflow.get_next_field()
                return {
                    'arabic': next_field['prompt_ar'],
                    'english': next_field['prompt_en'],
                    'field': next_field['name'],
                    'action': {
                        'type': 'fill_field',
                        'field': field_name,
                        'value': self.current_workflow.form_data[field_name]
                    },
                    'continue_conversation': True
                }
        
        return {
            'arabic': 'خطأ في المعالجة',
            'english': 'Processing error',
            'action': None,
            'continue_conversation': False
        }
        
    def _complete_form(self) -> Dict[str, Any]:
        """Complete form filling and submit"""
        self.in_form_filling = False
        
        return {
            'arabic': 'تم! جاري الإرسال...',
            'english': 'Done! Submitting...',
            'action': {
                'type': 'submit_form',
                'page': self.current_page,
                'data': self.current_workflow.form_data
            },
            'continue_conversation': False
        }
        
    def _extract_numbers(self, text: str) -> str:
        """Extract numbers from text"""
        arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        text = text.translate(arabic_to_english)
        return ''.join(c for c in text if c.isdigit())
        
    def _is_affirmative(self, text: str) -> bool:
        """Check if affirmative"""
        return any(word in text.lower() for word in ['نعم', 'yes', 'اه', 'تمام', 'ok'])
        
    def _normalize_arabic(self, text: str) -> str:
        """Normalize Arabic text"""
        replacements = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ة': 'ه', 'ى': 'ي'}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
        
    def reset(self):
        """Reset workflow"""
        if self.current_workflow:
            self.current_workflow.reset()
        self.current_workflow = None
        self.current_page = None
        self.in_form_filling = False


# Global instance
page_aware_manager = PageAwareConversationManager()

