/**
 * ═══════════════════════════════════════════════════════════════════
 * ABSHER CONVERSATIONAL VOICE AI - Full Multi-turn Dialogue System
 * ═══════════════════════════════════════════════════════════════════
 * 
 * Features:
 * - Full multi-turn conversations
 * - Wake-word detection ("أبشر")
 * - Complete service workflows
 * - Context-aware responses
 * - Form filling through voice
 * - Confirmation & error recovery
 */

class AbsherConversationalVoiceAI {
    constructor() {
        // Core components
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        
        // State
        this.isListening = false;
        this.inConversation = false;
        this.sessionId = this.generateSessionId();
        
        // Settings
        this.currentLanguage = 'ar-SA';
        this.wakeWord = 'أبشر';
        this.manualMode = true; // Click-to-talk enabled by default
        
        // Permissions
        this.hasPermission = false;
        
        // Initialize
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    async init() {
        console.log('🤖 Initializing Conversational Voice AI...');
        
        // Check browser support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('متصفحك لا يدعم التعرف على الصوت', 
                          'Your browser does not support speech recognition');
            return;
        }
        
        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure for conversational AI
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'ar-SA';
        this.recognition.maxAlternatives = 1;
        
        // Setup event listeners
        this.setupRecognitionListeners();
        
        // Update UI
        this.updateUI('idle');
        
        console.log('✅ Conversational AI Ready');
        
        // Welcome message
        this.showStatus('جاهز! انقر المايكروفون وتحدث', 'Ready! Click mic and speak', 'ℹ️');
    }
    
    setupRecognitionListeners() {
        this.recognition.onstart = () => {
            console.log('🎤 Listening...');
            this.isListening = true;
            this.updateUI('listening');
            this.showStatus('أستمع...', 'Listening...', '👂');
        };
        
        this.recognition.onresult = (event) => {
            const results = event.results[event.results.length - 1];
            const transcript = results[0].transcript.trim();
            const confidence = results[0].confidence;
            
            console.log('🗣️ Heard:', transcript, 'Confidence:', confidence);
            
            // Filter low confidence
            if (confidence < 0.45) {
                console.log('⚠️ Low confidence, ignoring');
                this.showStatus('لم أسمع بوضوح', 'Not clear', '🔇');
                this.updateUI('idle');
                return;
            }
            
            // Filter too short
            if (transcript.length < 2) {
                console.log('⚠️ Too short');
                this.updateUI('idle');
                return;
            }
            
            // Stop any ongoing speech
            this.synthesis.cancel();
            
            // Process the input
            this.processVoiceInput(transcript);
        };
        
        this.recognition.onerror = (event) => {
            console.error('❌ Recognition error:', event.error);
            
            if (event.error === 'not-allowed') {
                this.showPermissionBanner();
                this.hasPermission = false;
            } else if (event.error === 'no-speech') {
                this.showStatus('لم أسمع شيئاً', 'No speech detected', '🔇');
            } else {
                this.showError(`خطأ: ${event.error}`, `Error: ${event.error}`);
            }
            
            this.updateUI('error');
        };
        
        this.recognition.onend = () => {
            console.log('🎤 Recognition ended');
            this.isListening = false;
            
            // If in conversation, keep listening
            if (this.inConversation && this.manualMode === false) {
                setTimeout(() => {
                    if (this.inConversation) {
                        this.startListening();
                    }
                }, 500);
            } else if (!this.inConversation) {
                this.updateUI('idle');
            }
        };
    }
    
    // ═══════════════════════════════════════════════════════════
    // CONVERSATIONAL AI CORE
    // ═══════════════════════════════════════════════════════════
    
    async processVoiceInput(input) {
        console.log('💬 Processing:', input);
        
        this.updateUI('processing');
        this.showStatus('معالجة...', 'Processing...', '⏳');
        
        try {
            // Send to conversational AI backend
            const response = await fetch('/api/voice/conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input: input,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                await this.handleAIResponse(data.response);
            } else {
                this.showError('خطأ في المعالجة', 'Processing error');
                this.updateUI('error');
            }
            
        } catch (error) {
            console.error('❌ API Error:', error);
            this.showError('خطأ في الاتصال', 'Connection error');
            this.updateUI('error');
        }
    }
    
    async handleAIResponse(response) {
        console.log('🤖 AI Response:', response);
        
        // Speak the response
        await this.speak(response.arabic, response.english);
        
        // Handle action if any
        if (response.action) {
            await this.executeAction(response.action);
        }
        
        // Update conversation state
        if (response.continue_conversation) {
            this.inConversation = true;
            this.updateUI('active');
            
            // In manual mode, wait for next click
            // In wake word mode, keep listening
            if (!this.manualMode) {
                setTimeout(() => {
                    this.startListening();
                }, 1000);
            }
        } else {
            this.inConversation = false;
            this.updateUI('idle');
        }
    }
    
    async executeAction(action) {
        console.log('⚡ Executing action:', action);
        
        if (action.type === 'navigate') {
            // Navigate to page
            const pageUrls = {
                'violations': '/violations/',
                'id_renewal': '/id-renewal/',
                'passport': '/passport/',
                'driving_license': '/driving-license/',
                'vehicle_registration': '/vehicle-registration/',
                'employment': '/employment/',
                'health': '/health/',
                'education': '/education/',
                'services': '/services/',
                'index': '/'
            };
            
            const url = pageUrls[action.page];
            if (url) {
                // Show navigation message
                await new Promise(resolve => setTimeout(resolve, 1500));
                window.location.href = url;
            }
        }
        else if (action.type === 'fill_form') {
            // Fill form with collected data
            this.fillFormWithData(action.data);
        }
        else if (action.type === 'submit_form') {
            // Submit current form
            this.submitCurrentForm();
        }
    }
    
    fillFormWithData(data) {
        // Fill form fields with collected data
        for (const [key, value] of Object.entries(data)) {
            const input = document.querySelector(`[name="${key}"], #${key}`);
            if (input) {
                input.value = value;
                // Trigger change event
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    }
    
    submitCurrentForm() {
        // Find and submit the main form on page
        const form = document.querySelector('form.service-form, form#mainForm');
        if (form) {
            form.submit();
        }
    }
    
    // ═══════════════════════════════════════════════════════════
    // SPEECH SYNTHESIS
    // ═══════════════════════════════════════════════════════════
    
    speak(arabicText, englishText = '') {
        return new Promise((resolve) => {
            // Cancel any ongoing speech
            this.synthesis.cancel();
            
            // Turn off mic during speech (prevent echo)
            const wasListening = this.isListening;
            if (wasListening) {
                this.stopListening();
            }
            
            // Create utterance
            const utterance = new SpeechSynthesisUtterance(arabicText);
            utterance.lang = 'ar-SA';
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 0.9;
            
            utterance.onend = () => {
                console.log('🔊 Speech finished');
                resolve();
            };
            
            utterance.onerror = (error) => {
                console.error('🔊 Speech error:', error);
                resolve();
            };
            
            // Speak
            this.synthesis.speak(utterance);
            
            // Show status
            this.showStatus(arabicText, englishText || arabicText, '🔊');
        });
    }
    
    // ═══════════════════════════════════════════════════════════
    // CONTROLS
    // ═══════════════════════════════════════════════════════════
    
    async manualActivate() {
        console.log('👆 Manual activation');
        
        if (this.isListening) {
            // Stop listening
            this.stopListening();
        } else {
            // Start listening
            await this.startListening();
        }
    }
    
    async startListening() {
        if (this.isListening) return;
        
        try {
            await this.recognition.start();
            this.hasPermission = true;
            this.hidePermissionBanner();
        } catch (error) {
            console.error('❌ Start error:', error);
            if (error.name === 'NotAllowedError') {
                this.showPermissionBanner();
            }
        }
    }
    
    stopListening() {
        if (!this.isListening) return;
        
        try {
            this.recognition.stop();
        } catch (error) {
            console.error('❌ Stop error:', error);
        }
    }
    
    async resetConversation() {
        console.log('🔄 Resetting conversation');
        
        this.inConversation = false;
        this.updateUI('idle');
        
        try {
            await fetch('/api/voice/reset/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId
                })
            });
        } catch (error) {
            console.error('❌ Reset error:', error);
        }
    }
    
    toggleHelpPanel() {
        const panel = document.getElementById('voiceHelpPanel');
        if (panel) {
            panel.classList.toggle('show');
        }
    }
    
    // ═══════════════════════════════════════════════════════════
    // UI UPDATES
    // ═══════════════════════════════════════════════════════════
    
    updateUI(state) {
        const indicator = document.getElementById('voiceIndicator');
        if (!indicator) return;
        
        // Update button state
        indicator.className = 'voice-mic-button';
        indicator.classList.add(`state-${state}`);
        
        // Update status badge
        const statusTexts = {
            'idle': 'جاهز',
            'listening': 'أستمع...',
            'active': 'نشط',
            'processing': 'معالجة...',
            'error': 'خطأ'
        };
        
        const statusElement = indicator.querySelector('.voice-status-badge');
        if (statusElement) {
            statusElement.textContent = statusTexts[state] || 'جاهز';
        }
        
        // Show/hide waveform
        const waveform = document.getElementById('voiceWaveform');
        if (waveform) {
            if (state === 'listening') {
                waveform.classList.add('show');
            } else {
                waveform.classList.remove('show');
            }
        }
    }
    
    showStatus(arabicText, englishText, icon = '') {
        const statusEl = document.getElementById('voiceStatusMessage');
        if (!statusEl) return;
        
        statusEl.innerHTML = `
            <span class="status-icon">${icon}</span>
            <strong>${arabicText}</strong>
            ${englishText ? `<br><small>${englishText}</small>` : ''}
        `;
        statusEl.classList.add('show');
        
        setTimeout(() => {
            statusEl.classList.remove('show');
        }, 3500);
    }
    
    showError(arabicText, englishText) {
        this.showStatus(arabicText, englishText, '❌');
        this.updateUI('error');
        
        // Reset after error
        setTimeout(() => {
            this.updateUI('idle');
        }, 2000);
    }
    
    showPermissionBanner() {
        const banner = document.getElementById('voicePermissionBanner');
        if (banner) {
            banner.classList.add('show');
        }
    }
    
    hidePermissionBanner() {
        const banner = document.getElementById('voicePermissionBanner');
        if (banner) {
            banner.classList.remove('show');
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// INITIALIZE ON PAGE LOAD
// ═══════════════════════════════════════════════════════════════

let voiceAssistant = null;

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing Conversational Voice AI...');
    voiceAssistant = new AbsherConversationalVoiceAI();
    
    // Make globally accessible
    window.voiceAssistant = voiceAssistant;
    
    console.log('✅ Voice AI Ready!');
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AbsherConversationalVoiceAI;
}

