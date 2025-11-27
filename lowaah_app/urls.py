"""
URL configuration for Lowaah Sign Language Assistant app.
"""
from django.urls import path
from . import views

app_name = 'lowaah_app'

urlpatterns = [
    # Page routes
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('services/', views.services, name='services'),
    path('violations/', views.violations, name='violations'),
    path('id-renewal/', views.id_renewal, name='id_renewal'),
    path('absher-individuals/', views.absher_individuals, name='absher_individuals'),
    path('passport/', views.passport, name='passport'),
    path('driving-license/', views.driving_license, name='driving_license'),
    path('vehicle-registration/', views.vehicle_registration, name='vehicle_registration'),
    path('employment/', views.employment, name='employment'),
    path('health/', views.health, name='health'),
    path('education/', views.education, name='education'),
    path('success/', views.success, name='success'),
    path('test-camera/', views.test_camera, name='test_camera'),
    path('camera-test/', views.camera_test, name='camera_test'),
    path('gesture-help/', views.gesture_help, name='gesture_help'),
    
    # Profile routes
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('profile/select/', views.profile_selection, name='profile_selection'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/<str:profile_id>/', views.profile_detail, name='profile_detail'),
    
    # API routes
    path('api/detect-gesture/', views.detect_gesture, name='detect_gesture'),
    path('api/gesture-info/', views.gesture_info, name='gesture_info'),
    path('api/health/', views.health_check, name='health_check'),
    path('api/extract-card-info/', views.extract_card_info, name='extract_card_info'),
    
    # Profile API routes
    path('api/profiles/', views.api_profiles_list, name='api_profiles_list'),
    path('api/profile/<str:profile_id>/', views.api_profile_detail, name='api_profile_detail'),
    path('api/profile/create/', views.api_profile_create, name='api_profile_create'),
    path('api/profile/<str:profile_id>/add-car/', views.api_carplate_add, name='api_carplate_add'),
    
    # Sign Language Translation API routes
    path('api/translate/sign-to-text/', views.translate_sign_to_text, name='translate_sign_to_text'),
    path('api/translate/text-to-sign/', views.translate_text_to_sign, name='translate_text_to_sign'),
    path('api/translate/process-request/', views.process_service_request, name='process_service_request'),
    path('api/translate/clear-session/', views.clear_translation_session, name='clear_translation_session'),
    path('api/translate/status/', views.translation_system_status, name='translation_system_status'),
    
    # Voice AI Conversation API routes
    path('api/voice/conversation/', views.voice_conversation_api, name='voice_conversation'),
    path('api/voice/reset/', views.reset_voice_conversation, name='reset_voice_conversation'),
    path('api/voice/state/', views.get_conversation_state, name='get_conversation_state'),
    
    # Page-Aware Voice AI routes
    path('api/voice/page/start/', views.start_page_workflow, name='start_page_workflow'),
    path('api/voice/page/input/', views.process_page_field_input, name='process_page_field_input'),
    path('api/voice/page/reset/', views.reset_page_workflow, name='reset_page_workflow'),
]

