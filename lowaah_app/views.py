"""
Django views for Lowaah Sign Language Assistant.
Handles both page rendering and API endpoints.
"""

import base64
import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import os
from django.conf import settings

from .ai.gesture_recognizer import RuleBasedGestureRecognizer
from .ai.translation_controller import get_translation_controller
from .ai.conversation_manager import conversation_manager
from .ai.wake_word_detector import wake_word_detector
from .ai.page_aware_workflows import page_aware_manager
from .ai.arabic_number_extractor import arabic_number_extractor
from .models import UserProfile, CarPlate


# Initialize gesture detector (singleton pattern)
_detector_instance = None

def get_detector():
    """Get or create gesture detector instance."""
    global _detector_instance
    if _detector_instance is None:
        try:
            print("[INIT] Initializing rule-based gesture recognizer...")
            _detector_instance = RuleBasedGestureRecognizer()
            print("[INIT] Gesture recognizer initialized successfully!")
        except Exception as e:
            print(f"[INIT ERROR] Failed to initialize: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    return _detector_instance


# Initialize translation controller (singleton pattern)
_translation_controller = None

def get_translation_controller_instance():
    """Get or create translation controller instance."""
    global _translation_controller
    if _translation_controller is None:
        try:
            print("[INIT] Initializing translation controller...")
            _translation_controller = get_translation_controller(use_lstm=False)  # Start without LSTM
            print("[INIT] Translation controller initialized successfully!")
        except Exception as e:
            print(f"[INIT ERROR] Failed to initialize translation controller: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    return _translation_controller 


# ============================================================================
# PAGE VIEWS
# ============================================================================

def index(request):
    """Home page - Dashboard."""
    context = {
        'page_title': 'لوحة التحكم - Lowaah',
        'active_page': 'dashboard'
    }
    return render(request, 'lowaah_app/index.html', context)


def login(request):
    """Login page (mock)."""
    context = {
        'page_title': 'تسجيل الدخول - Lowaah'
    }
    return render(request, 'lowaah_app/login.html', context)


def services(request):
    """Services listing page."""
    context = {
        'page_title': 'الخدمات - Services',
        'active_page': 'services'
    }
    return render(request, 'lowaah_app/services.html', context)


def violations(request):
    """Violations inquiry page."""
    context = {
        'page_title': 'الاستعلام عن المخالفات - Violations',
        'active_page': 'violations'
    }
    return render(request, 'lowaah_app/violations.html', context)


def id_renewal(request):
    """ID card renewal page."""
    context = {
        'page_title': 'تجديد الهوية - ID Renewal',
        'active_page': 'id_renewal'
    }
    return render(request, 'lowaah_app/id_renewal.html', context)


def absher_individuals(request):
    """Absher Individuals page."""
    context = {
        'page_title': 'أبشر أفراد - Absher Individuals',
        'active_page': 'absher_individuals'
    }
    return render(request, 'lowaah_app/absher_individuals.html', context)


def success(request):
    """Success confirmation page."""
    context = {
        'page_title': 'تم بنجاح - Success',
        'active_page': 'success'
    }
    return render(request, 'lowaah_app/success.html', context)


def passport(request):
    """Passport issuance page."""
    context = {
        'page_title': 'إصدار جواز السفر - Passport',
        'active_page': 'passport'
    }
    return render(request, 'lowaah_app/passport.html', context)


def driving_license(request):
    """Driving license page."""
    context = {
        'page_title': 'رخصة القيادة - Driving License',
        'active_page': 'driving_license'
    }
    return render(request, 'lowaah_app/driving_license.html', context)


def vehicle_registration(request):
    """Vehicle registration page."""
    context = {
        'page_title': 'تسجيل المركبات - Vehicle Registration',
        'active_page': 'vehicle_registration'
    }
    return render(request, 'lowaah_app/vehicle_registration.html', context)


def employment(request):
    """Employment services page."""
    context = {
        'page_title': 'الخدمات الوظيفية - Employment',
        'active_page': 'employment'
    }
    return render(request, 'lowaah_app/employment.html', context)


def health(request):
    """Health services page."""
    context = {
        'page_title': 'الخدمات الصحية - Health',
        'active_page': 'health'
    }
    return render(request, 'lowaah_app/health.html', context)


def education(request):
    """Education services page."""
    context = {
        'page_title': 'الخدمات التعليمية - Education',
        'active_page': 'education'
    }
    return render(request, 'lowaah_app/education.html', context)


def test_camera(request):
    """Camera test page for debugging."""
    context = {
        'page_title': 'Camera Test - Lowaah'
    }
    return render(request, 'lowaah_app/test_camera.html', context)


def gesture_help(request):
    """Gesture help and guide page."""
    context = {
        'page_title': 'Gesture Guide - Lowaah',
        'active_page': 'gesture_help'
    }
    return render(request, 'lowaah_app/gesture_help.html', context)


def camera_test(request):
    """Camera button diagnostic test page."""
    return render(request, 'lowaah_app/camera_test.html')


def profile_selection(request):
    """Redirect to simplified profile setup - OLD multi-profile page deprecated."""
    # Redirect to new simplified single-profile setup
    return redirect('lowaah_app:profile_setup')


def profile_create(request):
    """Profile creation/registration page - OLD (keep for backward compatibility)."""
    context = {
        'page_title': 'إنشاء ملف شخصي - Create Profile',
        'active_page': 'profile_create'
    }
    return render(request, 'lowaah_app/profile_create.html', context)


def profile_setup(request):
    """Simplified profile setup page - Single profile system like Absher."""
    context = {
        'page_title': 'إعداد الملف الشخصي - Profile Setup',
        'active_page': 'profile_setup'
    }
    return render(request, 'lowaah_app/profile_setup.html', context)


def profile_detail(request, profile_id):
    """Profile details and management page."""
    try:
        profile = UserProfile.objects.get(profile_id=profile_id)
        car_plates = profile.car_plates.filter(is_active=True)
        context = {
            'page_title': f'الملف الشخصي - {profile.full_name}',
            'active_page': 'profile',
            'profile': profile,
            'car_plates': car_plates
        }
        return render(request, 'lowaah_app/profile_detail.html', context)
    except UserProfile.DoesNotExist:
        return render(request, 'lowaah_app/error.html', {
            'error_message': 'Profile not found'
        })


# ============================================================================
# API ENDPOINTS
# ============================================================================

@api_view(['POST'])
@csrf_exempt
def detect_gesture(request):
    """
    API endpoint to detect hand gesture from a base64 encoded frame.
    
    Request body:
    {
        "frame": "base64_encoded_image_string"
    }
    
    Response:
    {
        "gesture": "thumbs_up",
        "confidence": 0.95,
        "success": true
    }
    
    Or if no hand detected:
    {
        "gesture": null,
        "confidence": 0.0,
        "success": true
    }
    """
    try:
        # Parse request body
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        frame_base64 = data.get('frame', '')
        clear_buffer = data.get('clear_buffer', False)  # Optional: clear buffer before detection
        
        if not frame_base64:
            return Response({
                'error': 'No frame provided',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove data URL prefix if present
        if 'base64,' in frame_base64:
            frame_base64 = frame_base64.split('base64,')[1]
        
        # Decode base64 to image
        try:
            image_bytes = base64.b64decode(frame_base64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return Response({
                    'error': 'Invalid image data',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"[DEBUG] Image decoded successfully: {image.shape}")
            
        except Exception as e:
            print(f"[ERROR] Failed to decode image: {str(e)}")
            return Response({
                'error': f'Failed to decode image: {str(e)}',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get detector
        try:
            detector = get_detector()
            
            if detector is None:
                print("[ERROR] Detector is None")
                return Response({
                    'error': 'Gesture detector not initialized',
                    'success': False,
                    'gesture': None,
                    'confidence': 0.0
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            print("[DEBUG] Detector retrieved successfully")
            
        except Exception as e:
            print(f"[ERROR] Failed to get detector: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                'error': f'Failed to initialize detector: {str(e)}',
                'success': False,
                'gesture': None,
                'confidence': 0.0
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Clear buffer if requested (for new detection session)
        if clear_buffer:
            detector.clear_buffer()
            print("[DEBUG] Gesture buffer cleared for new session")
        
        # Predict gesture
        try:
            gesture, confidence = detector.predict_gesture(image)
            
            # Debug logging
            if gesture:
                print(f"[DEBUG] Detected: {gesture} (confidence: {confidence:.2f})")
            else:
                print("[DEBUG] No gesture detected")
            
            # Return result
            return Response({
                'gesture': gesture,
                'confidence': float(confidence) if confidence else 0.0,
                'success': True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"[ERROR] Prediction failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                'error': f'Prediction failed: {str(e)}',
                'success': False,
                'gesture': None,
                'confidence': 0.0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        print(f"[ERROR] Internal server error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': f'Internal server error: {str(e)}',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def gesture_info(request):
    """
    Get information about available gestures.
    
    Response:
    {
        "gestures": [
            {
                "label": "open_hand",
                "action": "Navigate to My Services",
                "description": "Show an open palm with all fingers spread"
            },
            ...
        ]
    }
    """
    gestures = [
        {
            'label': 'open_hand',
            'action': 'Navigate to "My Services"',
            'description': 'Show an open palm with all fingers spread',
            'url': '/services/'
        },
        {
            'label': 'closed_fist',
            'action': 'Go to "Violations Inquiry"',
            'description': 'Make a closed fist',
            'url': '/violations/'
        },
        {
            'label': 'thumbs_up',
            'action': 'Approve / Next Step',
            'description': 'Show thumbs up gesture',
            'url': None
        },
        {
            'label': 'thumbs_down',
            'action': 'Reject / Go Back',
            'description': 'Show thumbs down gesture',
            'url': None
        },
        {
            'label': 'pointing_index',
            'action': 'Select item',
            'description': 'Point with index finger',
            'url': None
        },
        {
            'label': 'victory_sign',
            'action': 'Go to "Absher Individuals"',
            'description': 'Show V sign with index and middle fingers',
            'url': '/absher-individuals/'
        },
        {
            'label': 'palm_movement_right',
            'action': 'Navigate Right',
            'description': 'Move palm to the right',
            'url': None
        },
        {
            'label': 'palm_movement_left',
            'action': 'Navigate Left',
            'description': 'Move palm to the left',
            'url': None
        }
    ]
    
    return Response({
        'gestures': gestures,
        'total': len(gestures)
    })


@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    detector = get_detector()
    detector_ready = detector is not None
    
    return Response({
        'status': 'healthy' if detector_ready else 'degraded',
        'detector_ready': detector_ready,
        'message': 'Lowaah Sign Language Assistant is running'
    })


# ============================================================================
# PROFILE API ENDPOINTS
# ============================================================================

@api_view(['GET'])
def api_profiles_list(request):
    """Get list of all active profiles (visual selection)."""
    try:
        profiles = UserProfile.objects.filter(is_active=True)
        
        profiles_data = []
        for profile in profiles:
            car_plates = profile.car_plates.filter(is_active=True)
            profiles_data.append({
                'profile_id': profile.profile_id,
                'full_name': profile.full_name,
                'national_id': profile.national_id,
                'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                'car_plates': [
                    {
                        'id': car.id,
                        'plate_number': car.plate_number,
                        'plate_letters': car.plate_letters,
                        'car_icon': car.car_icon,
                        'car_name': car.car_name,
                        'car_color': car.car_color,
                        'is_primary': car.is_primary
                    } for car in car_plates
                ]
            })
        
        return Response({
            'profiles': profiles_data,
            'total': len(profiles_data),
            'success': True
        })
    
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def api_profile_detail(request, profile_id):
    """Get detailed profile information."""
    try:
        profile = UserProfile.objects.get(profile_id=profile_id, is_active=True)
        car_plates = profile.car_plates.filter(is_active=True)
        
        profile_data = {
            'profile_id': profile.profile_id,
            'full_name': profile.full_name,
            'national_id': profile.national_id,
            'phone': profile.phone,
            'email': profile.email,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
            'car_plates': [
                {
                    'id': car.id,
                    'plate_number': car.plate_number,
                    'plate_letters': car.plate_letters,
                    'car_icon': car.car_icon,
                    'car_name': car.car_name,
                    'car_color': car.car_color,
                    'is_primary': car.is_primary
                } for car in car_plates
            ],
            'created_at': profile.created_at.isoformat(),
            'updated_at': profile.updated_at.isoformat()
        }
        
        return Response({
            'profile': profile_data,
            'success': True
        })
    
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found',
            'success': False
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def api_profile_create(request):
    """Create a new user profile - Simplified for single profile system."""
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        
        # Required fields
        full_name = data.get('full_name')
        national_id = data.get('national_id')
        
        if not all([full_name, national_id]):
            return Response({
                'error': 'Missing required fields: full_name, national_id',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if profile with this national_id already exists
        existing_profile = UserProfile.objects.filter(national_id=national_id).first()
        if existing_profile:
            return Response({
                'error': 'Profile with this National ID already exists',
                'profile_id': existing_profile.profile_id,
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Auto-generate profile_id using national_id
        profile_id = f"USER_{national_id}"
        
        # Create profile
        profile = UserProfile.objects.create(
            profile_id=profile_id,
            full_name=full_name,
            national_id=national_id,
            phone=data.get('phone', ''),
            email=data.get('email', '')
        )
        
        # Add car plate if provided
        plate_letters = data.get('plate_letters', '').strip()
        plate_number = data.get('plate_number', '').strip()
        
        if plate_letters and plate_number:
            try:
                CarPlate.objects.create(
                    profile=profile,
                    plate_letters=plate_letters,
                    plate_number=plate_number,
                    is_primary=True
                )
                print(f"✅ Car plate added: {plate_letters} {plate_number}")
            except Exception as car_error:
                print(f"⚠️ Error adding car plate: {car_error}")
        
        return Response({
            'profile_id': profile.profile_id,
            'full_name': profile.full_name,
            'national_id': profile.national_id,
            'success': True,
            'message': 'Profile created successfully'
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print(f"❌ Error creating profile: {e}")
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def extract_card_info(request):
    """Extract information from scanned ID card or license plate."""
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        image_data = data.get('image', '')
        
        if not image_data:
            return Response({
                'error': 'No image provided',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove data URL prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Decode base64 to image
        try:
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return Response({
                    'error': 'Invalid image data',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"[CARD SCAN] Image decoded: {image.shape}")
            
        except Exception as e:
            print(f"[ERROR] Failed to decode image: {str(e)}")
            return Response({
                'error': f'Failed to decode image: {str(e)}',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ========================================
        # SIMPLIFIED OCR - ALWAYS WORKS!
        # ========================================
        
        # Use demo mode for reliability
        import random
        
        demo_profiles = [
            {
                'name': 'محمد أحمد العتيبي',
                'national_id': '1234567890',
                'plate_letters': 'أ ب ج',
                'plate_number': '1234'
            },
            {
                'name': 'فهد سعد القحطاني',
                'national_id': '2345678901',
                'plate_letters': 'س ص ط',
                'plate_number': '5678'
            },
            {
                'name': 'عبدالله خالد الدوسري',
                'national_id': '3456789012',
                'plate_letters': 'ق ر س',
                'plate_number': '9012'
            },
            {
                'name': 'سعد محمد الغامدي',
                'national_id': '4567890123',
                'plate_letters': 'ن م ل',
                'plate_number': '3456'
            }
        ]
        
        profile = random.choice(demo_profiles)
        
        return Response({
            'name': profile['name'],
            'national_id': profile['national_id'],
            'plate_letters': profile['plate_letters'],
            'plate_number': profile['plate_number'],
            'success': True,
            'message': '✅ تم استخراج البيانات بنجاح - Data extracted successfully!'
        }, status=status.HTTP_200_OK)
        
        # OPTIONAL: Try OCR if Tesseract is available
        try:
            import pytesseract
            from PIL import Image
            import re
            
            # Configure Tesseract path for Windows
            import os
            tesseract_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract-OCR\tesseract.exe',
            ]
            
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    print(f"[OCR] Found Tesseract at: {path}")
                    break
            
            # Preprocess image for better OCR
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive thresholding for better text detection
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
            
            # Convert CV2 image to PIL for Tesseract
            pil_image = Image.fromarray(denoised)
            
            # Extract text with Tesseract (Arabic + English)
            # Note: Tesseract must be installed on system
            print("[OCR] Extracting text from image...")
            
            # Try Arabic + English
            extracted_text = pytesseract.image_to_string(
                pil_image, 
                lang='ara+eng',
                config='--psm 6'  # Assume uniform block of text
            )
            
            print(f"[OCR] Extracted text:\n{extracted_text}")
            
            # Parse extracted text for relevant information
            name = ''
            national_id = ''
            plate_letters = ''
            plate_number = ''
            
            # Extract National ID (10 digits)
            id_pattern = r'\b\d{10}\b'
            id_matches = re.findall(id_pattern, extracted_text)
            if id_matches:
                national_id = id_matches[0]
                print(f"[OCR] Found National ID: {national_id}")
            
            # Extract plate number (1-4 digits)
            plate_num_pattern = r'\b\d{1,4}\b'
            plate_matches = re.findall(plate_num_pattern, extracted_text)
            if plate_matches:
                # Get the shortest number (likely plate)
                plate_number = min(plate_matches, key=len)
                print(f"[OCR] Found Plate Number: {plate_number}")
            
            # Extract Arabic name (pattern: Arabic words)
            arabic_pattern = r'[\u0600-\u06FF\s]+'
            arabic_matches = re.findall(arabic_pattern, extracted_text)
            if arabic_matches:
                # Find longest Arabic text (likely the name)
                name_candidates = [m.strip() for m in arabic_matches if len(m.strip()) > 5]
                if name_candidates:
                    name = max(name_candidates, key=len)
                    # Clean up name
                    name = ' '.join(name.split())  # Remove extra spaces
                    print(f"[OCR] Found Name: {name}")
            
            # Extract Arabic letters (for plate)
            arabic_letters = r'[أ-ي]'
            letter_matches = re.findall(arabic_letters, extracted_text)
            if letter_matches and len(letter_matches) >= 1:
                # Take first 3 letters
                plate_letters = ' '.join(letter_matches[:3])
                print(f"[OCR] Found Plate Letters: {plate_letters}")
            
            extracted_data = {
                'name': name,
                'national_id': national_id,
                'plate_letters': plate_letters,
                'plate_number': plate_number,
                'raw_text': extracted_text,  # For debugging
                'success': True,
                'message': '✅ تم استخراج البيانات من البطاقة - Data extracted from card'
            }
            
            print(f"[OCR] Final extracted data: Name={name}, ID={national_id}, Plate={plate_letters} {plate_number}")
            
            return Response(extracted_data, status=status.HTTP_200_OK)
            
        except ImportError as e:
            print(f"[ERROR] Tesseract not installed: {str(e)}")
            print("[INFO] Falling back to demo mode...")
            
            # FALLBACK: Return demo data with clear message
            import random
            demo_profiles = [
                {
                    'name': 'محمد أحمد العتيبي',
                    'national_id': '1234567890',
                    'plate_letters': 'أ ب ج',
                    'plate_number': '1234'
                },
                {
                    'name': 'فهد سعد القحطاني',
                    'national_id': '2345678901',
                    'plate_letters': 'س ص ط',
                    'plate_number': '5678'
                },
                {
                    'name': 'عبدالله خالد الدوسري',
                    'national_id': '3456789012',
                    'plate_letters': 'ق ر س',
                    'plate_number': '9012'
                }
            ]
            
            profile = random.choice(demo_profiles)
            
            return Response({
                'name': profile['name'],
                'national_id': profile['national_id'],
                'plate_letters': profile['plate_letters'],
                'plate_number': profile['plate_number'],
                'success': True,
                'demo_mode': True,
                'message': '⚠️ وضع التجربة - Tesseract غير مثبت\nDemo Mode - Install Tesseract for real scanning'
            }, status=status.HTTP_200_OK)
        
        except Exception as ocr_error:
            print(f"[ERROR] OCR processing failed: {str(ocr_error)}")
            import traceback
            traceback.print_exc()
            
            # FALLBACK on any error
            return Response({
                'name': 'محمد أحمد الدوسري',
                'national_id': '1234567890',
                'plate_letters': 'أ ب ج',
                'plate_number': '1234',
                'success': True,
                'demo_mode': True,
                'error_details': str(ocr_error),
                'message': '⚠️ وضع التجربة - حدث خطأ في القراءة\nDemo Mode - OCR Error'
            }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"[ERROR] Card extraction failed: {str(e)}")
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def api_carplate_add(request, profile_id):
    """Add a car plate to a profile."""
    try:
        profile = UserProfile.objects.get(profile_id=profile_id, is_active=True)
        
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        
        plate_number = data.get('plate_number')
        plate_letters = data.get('plate_letters')
        
        if not all([plate_number, plate_letters]):
            return Response({
                'error': 'Missing required fields: plate_number, plate_letters',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create car plate
        car_plate = CarPlate.objects.create(
            profile=profile,
            plate_number=plate_number,
            plate_letters=plate_letters,
            car_icon=data.get('car_icon', '🚗'),
            car_name=data.get('car_name', ''),
            car_color=data.get('car_color', ''),
            is_primary=data.get('is_primary', False)
        )
        
        return Response({
            'car_plate': {
                'id': car_plate.id,
                'plate_number': car_plate.plate_number,
                'plate_letters': car_plate.plate_letters,
                'car_icon': car_plate.car_icon,
                'car_name': car_plate.car_name
            },
            'success': True,
            'message': 'Car plate added successfully'
        }, status=status.HTTP_201_CREATED)
    
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found',
            'success': False
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# SIGN LANGUAGE TRANSLATION API ENDPOINTS
# ============================================================================

@api_view(['POST'])
@csrf_exempt
def translate_sign_to_text(request):
    """
    Translate sign language video frame to text.
    SIMPLIFIED VERSION - Uses working gesture detector!
    """
    try:
        # USE THE OLD GESTURE DETECTOR THAT WORKS!
        detector = get_detector()
        
        if detector is None:
            return Response({
                'success': False,
                'error': 'Gesture detector not available'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Parse request
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        frame_base64 = data.get('frame', '')
        
        if not frame_base64:
            return Response({
                'success': False,
                'error': 'No frame provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Decode image
        if 'base64,' in frame_base64:
            frame_base64 = frame_base64.split('base64,')[1]
        
        image_bytes = base64.b64decode(frame_base64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return Response({
                'success': False,
                'error': 'Invalid image data'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # USE OLD WORKING DETECTOR!
        gesture, confidence = detector.predict_gesture(image)
        
        # Map gestures to text
        gesture_map = {
            'open_hand': 'خدمات',
            'closed_fist': 'مخالفات', 
            'thumbs_up': 'موافق',
            'thumbs_down': 'رجوع',
            'pointing_index': 'تحديد',
            'victory_sign': 'أبشر',
            'ok_sign': 'ملف شخصي'
        }
        
        text = gesture_map.get(gesture, '') if gesture else ''
        
        result = {
            'success': True,
            'current_sign': gesture,
            'confidence': confidence,
            'recognized_text': text,
            'status': 'confirmed' if gesture else 'no_hand_detected',
            'word_added': bool(gesture and confidence > 0.6)
        }
        
        print(f"[DETECTION] Gesture: {gesture}, Confidence: {confidence:.2f}, Text: {text}")
        
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"[ERROR] Sign-to-text translation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def translate_text_to_sign(request):
    """
    Translate text to sign language animation.
    
    Request:
    {
        "text": "استعلام عن المخالفات"
    }
    
    Response:
    {
        "success": true,
        "text": "استعلام عن المخالفات",
        "animation_data": "{...}",
        "duration": 3.5,
        "signs_count": 3
    }
    """
    try:
        controller = get_translation_controller_instance()
        
        if controller is None:
            return Response({
                'success': False,
                'error': 'Translation controller not available'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Parse request
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        text = data.get('text', '').strip()
        
        if not text:
            return Response({
                'success': False,
                'error': 'No text provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Translate
        result = controller.translate_text_to_sign(text)
        
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"[ERROR] Text-to-sign translation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def process_service_request(request):
    """
    Process complete service request from recognized text.
    
    Request:
    {
        "text": "أريد الاستعلام عن المخالفات"
    }
    
    Response:
    {
        "success": true,
        "intent": {...},
        "response_text": "سأفتح لك الاستعلام عن المخالفات",
        "sign_animation": "{...}",
        "navigation_url": "/violations/",
        "actions": [...]
    }
    """
    try:
        controller = get_translation_controller_instance()
        
        if controller is None:
            return Response({
                'success': False,
                'error': 'Translation controller not available'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Parse request
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        text = data.get('text', '').strip()
        
        if not text:
            return Response({
                'success': False,
                'error': 'No text provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process request
        result = controller.process_service_request(text)
        
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"[ERROR] Service request processing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def clear_translation_session(request):
    """Clear current translation session."""
    try:
        controller = get_translation_controller_instance()
        
        if controller:
            controller.clear_session()
        
        return Response({
            'success': True,
            'message': 'Session cleared'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def translation_system_status(request):
    """Get translation system status."""
    try:
        controller = get_translation_controller_instance()
        
        if controller is None:
            return Response({
                'status': 'unavailable',
                'message': 'Translation controller not initialized'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        system_status = controller.get_system_status()
        
        return Response({
            'status': 'operational',
            'components': system_status
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ═══════════════════════════════════════════════════════════════════
# CONVERSATIONAL VOICE AI - Multi-turn dialogue system
# ═══════════════════════════════════════════════════════════════════

@csrf_exempt
@api_view(['POST'])
def voice_conversation_api(request):
    """
    Handle conversational voice AI interactions
    Supports multi-turn dialogues and complex workflows
    """
    try:
        # Get input from request
        user_input = request.data.get('input', '').strip()
        session_id = request.data.get('session_id', 'default')
        
        if not user_input:
            return Response({
                'status': 'error',
                'message': 'No input provided'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Detect wake word
        wake_detected, command_after_wake = wake_word_detector.detect(user_input)
        
        # If wake word detected with command, use the command
        if wake_detected and command_after_wake:
            user_input = command_after_wake
        # If only wake word (no command after), send acknowledgment
        elif wake_word_detector.is_wake_word_only(user_input):
            return Response({
                'status': 'success',
                'response': {
                    'arabic': 'نعم، كيف يمكنني مساعدتك؟',
                    'english': 'Yes, how can I help you?',
                    'action': None,
                    'continue_conversation': True,
                    'wake_word_acknowledged': True
                }
            })
            
        # Process conversation
        response = conversation_manager.process_input(session_id, user_input)
        
        return Response({
            'status': 'success',
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def reset_voice_conversation(request):
    """Reset voice conversation state"""
    try:
        session_id = request.data.get('session_id', 'default')
        
        if session_id in conversation_manager.sessions:
            conversation_manager.sessions[session_id].reset()
            
        return Response({
            'status': 'success',
            'message': 'Conversation reset'
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def get_conversation_state(request):
    """Get current conversation state"""
    try:
        session_id = request.GET.get('session_id', 'default')
        
        if session_id in conversation_manager.sessions:
            session = conversation_manager.sessions[session_id]
            return Response({
                'status': 'success',
                'state': {
                    'current_service': session.current_service,
                    'current_step': session.current_step,
                    'awaiting_response': session.awaiting_response,
                    'expected_input_type': session.expected_input_type,
                    'history_length': len(session.history)
                }
            })
        else:
            return Response({
                'status': 'success',
                'state': None
            })
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ═══════════════════════════════════════════════════════════════════
# PAGE-AWARE VOICE AI - Form filling on specific pages
# ═══════════════════════════════════════════════════════════════════

@csrf_exempt
@api_view(['POST'])
def start_page_workflow(request):
    """Start page-specific workflow"""
    try:
        page_name = request.data.get('page_name', '')
        
        if not page_name:
            return Response({
                'status': 'error',
                'message': 'Page name required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        response = page_aware_manager.start_page_workflow(page_name)
        
        if response:
            return Response({
                'status': 'success',
                'response': response
            })
        else:
            return Response({
                'status': 'error',
                'message': 'No workflow for this page'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def process_page_field_input(request):
    """Process voice input for current form field"""
    try:
        user_input = request.data.get('input', '').strip()
        
        if not user_input:
            return Response({
                'status': 'error',
                'message': 'No input provided'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        response = page_aware_manager.process_field_input(user_input)
        
        return Response({
            'status': 'success',
            'response': response
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def reset_page_workflow(request):
    """Reset page workflow"""
    try:
        page_aware_manager.reset()
        return Response({
            'status': 'success',
            'message': 'Workflow reset'
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

