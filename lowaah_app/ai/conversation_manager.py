"""
Conversation Manager - Multi-turn dialogue system
Handles conversation state, context, and flow management
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class ConversationState:
    """Manages conversation state for a single user session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.context = {}
        self.history = []
        self.current_service = None
        self.current_step = None
        self.collected_data = {}
        self.last_interaction = datetime.now()
        self.awaiting_response = False
        self.expected_input_type = None
        self.retry_count = 0
        
    def add_turn(self, user_input: str, assistant_response: str):
        """Add a conversation turn"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'assistant': assistant_response
        })
        self.last_interaction = datetime.now()
        
    def set_service(self, service: str, step: str = 'start'):
        """Set current service and step"""
        self.current_service = service
        self.current_step = step
        self.collected_data = {}
        
    def update_data(self, key: str, value: Any):
        """Update collected data"""
        self.collected_data[key] = value
        
    def get_data(self, key: str) -> Any:
        """Get collected data"""
        return self.collected_data.get(key)
        
    def set_expecting(self, input_type: str):
        """Set what type of input we're expecting"""
        self.awaiting_response = True
        self.expected_input_type = input_type
        
    def clear_expecting(self):
        """Clear expectation"""
        self.awaiting_response = False
        self.expected_input_type = None
        self.retry_count = 0
        
    def is_active(self) -> bool:
        """Check if conversation is still active (within 5 minutes)"""
        return (datetime.now() - self.last_interaction).seconds < 300
        
    def reset(self):
        """Reset conversation state"""
        self.current_service = None
        self.current_step = None
        self.collected_data = {}
        self.awaiting_response = False
        self.expected_input_type = None
        self.retry_count = 0


class ConversationManager:
    """Main conversation management system"""
    
    def __init__(self):
        self.sessions: Dict[str, ConversationState] = {}
        
    def get_or_create_session(self, session_id: str) -> ConversationState:
        """Get existing session or create new one"""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationState(session_id)
        return self.sessions[session_id]
        
    def process_input(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Process user input and generate response"""
        session = self.get_or_create_session(session_id)
        
        # SILENCE DETECTION: Check if input is empty or too short
        if not user_input or len(user_input.strip()) < 2:
            # User didn't say anything or very unclear
            session.retry_count += 1
            
            if session.retry_count >= 3:
                # Too many retries, reset
                return self._handle_too_many_retries(session)
            
            return {
                'arabic': 'لم أسمع إجابة. هل تكرر طلبك من فضلك؟',
                'english': 'I did not hear an answer. Could you repeat your request please?',
                'action': None,
                'continue_conversation': True,
                'silence_detected': True
            }
        
        # Reset retry count on valid input
        session.retry_count = 0
        
        # Normalize input
        normalized_input = self._normalize_arabic(user_input.lower().strip())
        
        # Check if we're awaiting a specific response
        if session.awaiting_response:
            return self._handle_expected_response(session, normalized_input)
        
        # Check for service intent
        service_intent = self._detect_service_intent(normalized_input)
        
        if service_intent:
            return self._start_service_workflow(session, service_intent, normalized_input)
        
        # Check for general queries
        general_response = self._handle_general_query(session, normalized_input)
        if general_response:
            return general_response
        
        # Fallback - but don't guess randomly!
        return self._generate_fallback_response(session)
        
    def _normalize_arabic(self, text: str) -> str:
        """Normalize Arabic text"""
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
            'ة': 'ه',
            'ى': 'ي',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
        
    def _detect_service_intent(self, text: str) -> Optional[str]:
        """Detect which service user wants"""
        
        # Violations
        if any(word in text for word in ['مخالف', 'مخالفه', 'مخالفات', 'غرام', 'غرامه', 'violation']):
            return 'violations'
            
        # ID Renewal
        if any(word in text for word in ['هويه', 'هوية', 'بطاقه', 'تجديد', 'renew', 'id', 'identity']):
            return 'id_renewal'
            
        # Passport
        if any(word in text for word in ['جواز', 'سفر', 'passport']):
            return 'passport'
            
        # Driving License
        if any(word in text for word in ['رخصه', 'رخصة', 'قياده', 'قيادة', 'license', 'driving']):
            return 'driving_license'
            
        # Vehicle Registration
        if any(word in text for word in ['مركبه', 'مركبة', 'سياره', 'سيارة', 'vehicle', 'car']):
            return 'vehicle'
            
        # Employment
        if any(word in text for word in ['توظيف', 'وظيفه', 'عمل', 'employment', 'work']):
            return 'employment'
            
        # Health
        if any(word in text for word in ['صحه', 'صحة', 'طبي', 'علاج', 'health', 'medical']):
            return 'health'
            
        # Education
        if any(word in text for word in ['تعليم', 'دراسه', 'مدرسه', 'education', 'school']):
            return 'education'
            
        return None
        
    def _start_service_workflow(self, session: ConversationState, 
                                service: str, user_input: str) -> Dict[str, Any]:
        """Start a service workflow"""
        session.set_service(service, 'start')
        
        workflows = {
            'violations': self._violations_workflow,
            'id_renewal': self._id_renewal_workflow,
            'passport': self._passport_workflow,
            'driving_license': self._driving_license_workflow,
            'vehicle': self._vehicle_workflow,
            'employment': self._employment_workflow,
            'health': self._health_workflow,
            'education': self._education_workflow,
        }
        
        workflow = workflows.get(service)
        if workflow:
            return workflow(session, 'start', user_input)
        
        return self._generate_fallback_response(session)
        
    # ═══════════════════════════════════════════════════════════
    # SERVICE WORKFLOWS - Multi-turn conversations
    # ═══════════════════════════════════════════════════════════
    
    def _violations_workflow(self, session: ConversationState, 
                            step: str, user_input: str) -> Dict[str, Any]:
        """Violations check workflow"""
        
        if step == 'start':
            # Just navigate - don't ask for fields yet
            session.clear_expecting()
            
            response = {
                'arabic': 'حسناً، سأفتح صفحة المخالفات',
                'english': 'Opening violations page',
                'action': {
                    'type': 'navigate',
                    'page': 'violations',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        elif step == 'ask_id_type':
            # Check if user said ID or plate
            if 'هوي' in user_input or 'بطاق' in user_input or 'id' in user_input:
                session.update_data('search_type', 'id')
                session.current_step = 'ask_id_number'
                session.set_expecting('id_number')
                
                response = {
                    'arabic': 'ممتاز. الآن قل رقم الهوية من فضلك، رقم برقم بوضوح',
                    'english': 'Please say your ID number, digit by digit',
                    'action': None,
                    'continue_conversation': True
                }
                
            elif 'لوح' in user_input or 'plate' in user_input:
                session.update_data('search_type', 'plate')
                session.current_step = 'ask_plate_number'
                session.set_expecting('plate_number')
                
                response = {
                    'arabic': 'حسناً، قل رقم اللوحة من فضلك',
                    'english': 'Please say the plate number',
                    'action': None,
                    'continue_conversation': True
                }
            else:
                # Didn't understand
                session.retry_count += 1
                if session.retry_count > 2:
                    return self._handle_too_many_retries(session)
                    
                response = {
                    'arabic': 'لم أفهم. قل "رقم الهوية" أو "رقم اللوحة"',
                    'english': 'Please say "ID number" or "plate number"',
                    'action': None,
                    'continue_conversation': True
                }
                
        elif step == 'ask_id_number':
            # Extract numbers from input
            id_number = self._extract_numbers(user_input)
            
            if len(id_number) == 10:
                session.update_data('id_number', id_number)
                session.current_step = 'confirm_search'
                session.set_expecting('confirmation')
                
                response = {
                    'arabic': f'رقم الهوية {id_number}. هل هذا صحيح؟ قل نعم أو لا',
                    'english': f'ID number {id_number}. Is this correct? Say yes or no',
                    'action': None,
                    'continue_conversation': True
                }
            else:
                session.retry_count += 1
                if session.retry_count > 2:
                    return self._handle_too_many_retries(session)
                    
                response = {
                    'arabic': 'رقم الهوية غير صحيح. يجب أن يكون 10 أرقام. حاول مرة أخرى',
                    'english': 'ID must be 10 digits. Try again',
                    'action': None,
                    'continue_conversation': True
                }
                
        elif step == 'confirm_search':
            if self._is_affirmative(user_input):
                # Execute search
                session.clear_expecting()
                
                response = {
                    'arabic': 'جاري البحث عن المخالفات...',
                    'english': 'Searching for violations...',
                    'action': {
                        'type': 'navigate',
                        'page': 'violations',
                        'data': session.collected_data
                    },
                    'continue_conversation': False
                }
                
                session.reset()
                
            elif self._is_negative(user_input):
                # Restart
                session.current_step = 'ask_id_number'
                session.retry_count = 0
                
                response = {
                    'arabic': 'حسناً، قل رقم الهوية مرة أخرى من فضلك',
                    'english': 'Please say the ID number again',
                    'action': None,
                    'continue_conversation': True
                }
            else:
                response = {
                    'arabic': 'قل "نعم" للتأكيد أو "لا" للإعادة',
                    'english': 'Say "yes" to confirm or "no" to retry',
                    'action': None,
                    'continue_conversation': True
                }
                
        else:
            response = self._generate_fallback_response(session)
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _id_renewal_workflow(self, session: ConversationState, 
                            step: str, user_input: str) -> Dict[str, Any]:
        """ID renewal workflow"""
        
        if step == 'start':
            # Just navigate - form filling happens on page
            session.clear_expecting()
            
            response = {
                'arabic': 'سأفتح صفحة تجديد الهوية',
                'english': 'Opening ID renewal page',
                'action': {
                    'type': 'navigate',
                    'page': 'id_renewal',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        elif step == 'ask_id_number':
            id_number = self._extract_numbers(user_input)
            
            if len(id_number) == 10:
                session.update_data('id_number', id_number)
                session.current_step = 'ask_upload_photo'
                session.set_expecting('confirmation')
                
                response = {
                    'arabic': f'رقم الهوية {id_number}. هل معك صورة الهوية؟ قل نعم أو لا',
                    'english': f'ID {id_number}. Do you have ID photo? Yes or no',
                    'action': None,
                    'continue_conversation': True
                }
            else:
                response = {
                    'arabic': 'رقم الهوية يجب أن يكون 10 أرقام. حاول مرة أخرى',
                    'english': 'ID must be 10 digits. Try again',
                    'action': None,
                    'continue_conversation': True
                }
                
        elif step == 'ask_upload_photo':
            if self._is_affirmative(user_input):
                session.clear_expecting()
                
                response = {
                    'arabic': 'ممتاز! سأفتح صفحة تجديد الهوية. استخدم الكاميرا لتصوير الهوية',
                    'english': 'Opening ID renewal page. Use camera to scan ID',
                    'action': {
                        'type': 'navigate',
                        'page': 'id_renewal',
                        'data': session.collected_data
                    },
                    'continue_conversation': False
                }
                
                session.reset()
                
            else:
                session.clear_expecting()
                
                response = {
                    'arabic': 'لا بأس. احضر صورة الهوية أولاً ثم عد مرة أخرى. قل "أبشر" عندما تكون جاهزاً',
                    'english': 'No problem. Get your ID photo first, then say "Absher" when ready',
                    'action': None,
                    'continue_conversation': False
                }
                
                session.reset()
                
        else:
            response = self._generate_fallback_response(session)
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _passport_workflow(self, session: ConversationState, 
                          step: str, user_input: str) -> Dict[str, Any]:
        """Passport services workflow"""
        
        if step == 'start':
            session.current_step = 'ask_action'
            session.set_expecting('passport_action')
            
            response = {
                'arabic': 'خدمات جواز السفر. هل تريد: إصدار جديد، تجديد، أو استعلام؟',
                'english': 'Passport services. New issue, renewal, or inquiry?',
                'action': None,
                'continue_conversation': True
            }
            
        elif step == 'ask_action':
            if 'جديد' in user_input or 'اصدار' in user_input or 'new' in user_input:
                action = 'new'
            elif 'تجديد' in user_input or 'renew' in user_input:
                action = 'renewal'
            elif 'استعلام' in user_input or 'inquiry' in user_input:
                action = 'inquiry'
            else:
                response = {
                    'arabic': 'قل: "إصدار جديد"، "تجديد"، أو "استعلام"',
                    'english': 'Say: "new issue", "renewal", or "inquiry"',
                    'action': None,
                    'continue_conversation': True
                }
                session.add_turn(user_input, response['arabic'])
                return response
                
            session.update_data('passport_action', action)
            session.clear_expecting()
            
            response = {
                'arabic': f'سأفتح صفحة جواز السفر - {action}',
                'english': f'Opening passport page - {action}',
                'action': {
                    'type': 'navigate',
                    'page': 'passport',
                    'data': session.collected_data
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        else:
            response = self._generate_fallback_response(session)
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _driving_license_workflow(self, session: ConversationState, 
                                  step: str, user_input: str) -> Dict[str, Any]:
        """Driving license workflow"""
        
        if step == 'start':
            session.clear_expecting()
            
            response = {
                'arabic': 'سأفتح صفحة خدمات رخصة القيادة',
                'english': 'Opening driving license services',
                'action': {
                    'type': 'navigate',
                    'page': 'driving_license',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _vehicle_workflow(self, session: ConversationState, 
                         step: str, user_input: str) -> Dict[str, Any]:
        """Vehicle registration workflow"""
        
        if step == 'start':
            session.clear_expecting()
            
            response = {
                'arabic': 'سأفتح صفحة خدمات تسجيل المركبات',
                'english': 'Opening vehicle registration services',
                'action': {
                    'type': 'navigate',
                    'page': 'vehicle_registration',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _employment_workflow(self, session: ConversationState, 
                            step: str, user_input: str) -> Dict[str, Any]:
        """Employment services workflow"""
        
        if step == 'start':
            session.clear_expecting()
            
            response = {
                'arabic': 'سأفتح صفحة خدمات التوظيف',
                'english': 'Opening employment services',
                'action': {
                    'type': 'navigate',
                    'page': 'employment',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _health_workflow(self, session: ConversationState, 
                        step: str, user_input: str) -> Dict[str, Any]:
        """Health services workflow"""
        
        if step == 'start':
            session.clear_expecting()
            
            response = {
                'arabic': 'سأفتح صفحة الخدمات الصحية',
                'english': 'Opening health services',
                'action': {
                    'type': 'navigate',
                    'page': 'health',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    def _education_workflow(self, session: ConversationState, 
                           step: str, user_input: str) -> Dict[str, Any]:
        """Education services workflow"""
        
        if step == 'start':
            session.clear_expecting()
            
            response = {
                'arabic': 'سأفتح صفحة الخدمات التعليمية',
                'english': 'Opening education services',
                'action': {
                    'type': 'navigate',
                    'page': 'education',
                    'data': {}
                },
                'continue_conversation': False
            }
            
            session.reset()
            
        session.add_turn(user_input, response['arabic'])
        return response
        
    # ═══════════════════════════════════════════════════════════
    # HELPER METHODS
    # ═══════════════════════════════════════════════════════════
    
    def _handle_expected_response(self, session: ConversationState, 
                                  user_input: str) -> Dict[str, Any]:
        """Handle response when we're expecting specific input"""
        # Delegate to current workflow
        workflow_method = getattr(self, f'_{session.current_service}_workflow', None)
        if workflow_method:
            return workflow_method(session, session.current_step, user_input)
        return self._generate_fallback_response(session)
        
    def _handle_general_query(self, session: ConversationState, 
                             user_input: str) -> Optional[Dict[str, Any]]:
        """Handle general queries"""
        
        # Help request
        if any(word in user_input for word in ['مساعده', 'help', 'ساعد']):
            return {
                'arabic': 'يمكنني مساعدتك في: المخالفات، تجديد الهوية، جواز السفر، رخصة القيادة، والمزيد. قل اسم الخدمة',
                'english': 'I can help with: violations, ID renewal, passport, driving license, and more',
                'action': None,
                'continue_conversation': False
            }
            
        # Services list
        if any(word in user_input for word in ['خدمات', 'services']):
            return {
                'arabic': 'الخدمات المتاحة: المخالفات، الهوية، جواز السفر، رخصة القيادة، المركبات، التوظيف، الصحة، التعليم',
                'english': 'Available services: violations, ID, passport, driving, vehicles, employment, health, education',
                'action': {
                    'type': 'navigate',
                    'page': 'services',
                    'data': {}
                },
                'continue_conversation': False
            }
            
        # Home
        if any(word in user_input for word in ['رئيسيه', 'home', 'بدايه']):
            return {
                'arabic': 'سأعيدك إلى الصفحة الرئيسية',
                'english': 'Taking you to home page',
                'action': {
                    'type': 'navigate',
                    'page': 'index',
                    'data': {}
                },
                'continue_conversation': False
            }
            
        return None
        
    def _generate_fallback_response(self, session: ConversationState) -> Dict[str, Any]:
        """Generate fallback response when we don't understand"""
        return {
            'arabic': 'عذراً، لم أفهم. قل "مساعدة" لرؤية الخدمات المتاحة، أو قل اسم الخدمة مباشرة',
            'english': 'Sorry, I did not understand. Say "help" for services, or say service name',
            'action': None,
            'continue_conversation': False
        }
        
    def _handle_too_many_retries(self, session: ConversationState) -> Dict[str, Any]:
        """Handle too many failed attempts"""
        session.reset()
        return {
            'arabic': 'عذراً، حدث خطأ. سأبدأ من جديد. قل "أبشر" لتبدأ مرة أخرى',
            'english': 'Sorry, error occurred. Say "Absher" to start again',
            'action': None,
            'continue_conversation': False
        }
        
    def _extract_numbers(self, text: str) -> str:
        """Extract numbers from text"""
        # Convert Arabic numerals to English
        arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        text = text.translate(arabic_to_english)
        
        # Extract only digits
        numbers = ''.join(c for c in text if c.isdigit())
        return numbers
        
    def _is_affirmative(self, text: str) -> bool:
        """Check if response is affirmative"""
        affirmative_words = ['نعم', 'yes', 'اه', 'تمام', 'ايوه', 'صح', 'ok', 'موافق']
        return any(word in text for word in affirmative_words)
        
    def _is_negative(self, text: str) -> bool:
        """Check if response is negative"""
        negative_words = ['لا', 'no', 'لأ', 'كلا', 'غلط', 'خطأ']
        return any(word in text for word in negative_words)


# Global conversation manager instance
conversation_manager = ConversationManager()

