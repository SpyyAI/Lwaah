/**
 * ═══════════════════════════════════════════════════════════════════
 * ABSHER CONTINUOUS VOICE AI - Always Listening + Page-Aware Form Filling
 * ═══════════════════════════════════════════════════════════════════
 * 
 * Features:
 * - Continuous wake word listening (no button click)
 * - "أبشر" wake word detection
 * - Navigate to service pages
 * - Continue conversation ON the page
 * - Fill form fields field-by-field
 * - Submit when complete
 */

class AbsherContinuousVoiceAI {
    constructor() {
        // Core components
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        
        // State
        this.isListening = false;
        this.inConversation = false;
        this.onPage = false;
        this.inFormFilling = false;
        this.sessionId = this.generateSessionId();
        this.currentFieldIndex = 0;
        this.currentFieldName = null;
        
        // Settings
        this.currentLanguage = 'ar-SA';
        this.wakeWord = 'أبشر';
        this.continuousMode = true; // ALWAYS LISTENING
        
        // Silence detection
        this.silenceTimeout = null;
        this.silenceDelay = 4000; // 4 seconds
        this.noSpeechCount = 0;
        this.maxNoSpeech = 3;
        
        // Current page
        this.currentPage = this.detectCurrentPage();
        
        // Initialize
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    detectCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('/violations')) return 'violations';
        if (path.includes('/id-renewal')) return 'id_renewal';
        if (path.includes('/passport')) return 'passport';
        if (path.includes('/driving-license')) return 'driving_license';
        if (path.includes('/vehicle-registration')) return 'vehicle_registration';
        return null;
    }
    
    async init() {
        console.log('🤖 Initializing Continuous Voice AI...');
        
        // Check browser support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('متصفحك لا يدعم التعرف على الصوت', 
                          'Your browser does not support speech recognition');
            return;
        }
        
        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure for continuous listening
        this.recognition.continuous = false; // Restart after each result
        this.recognition.interimResults = false;
        this.recognition.lang = 'ar-SA';
        this.recognition.maxAlternatives = 1;
        
        // Setup listeners
        this.setupRecognitionListeners();
        
        // Update UI
        this.updateUI('idle');
        
        console.log('✅ Continuous AI Ready');
        
        // Check if on service page
        if (this.currentPage) {
            console.log('📄 On service page:', this.currentPage);
            
            // AUTO-START page workflow after small delay
            setTimeout(() => {
                console.log('🚀 Auto-starting page workflow...');
                this.startPageWorkflow();
            }, 2000); // 2 seconds after page load
        } else {
            // Start listening for wake word
            this.startContinuousListening();
        }
    }
    
    setupRecognitionListeners() {
        this.recognition.onstart = () => {
            console.log('🎤 Listening...');
            this.isListening = true;
            this.updateUI('listening');
        };
        
        this.recognition.onresult = (event) => {
            const results = event.results[event.results.length - 1];
            const transcript = results[0].transcript.trim();
            const confidence = results[0].confidence;
            
            console.log('🗣️ Heard:', transcript, 'Confidence:', confidence);
            console.log('📊 Current state: inConversation=' + this.inConversation + ', inFormFilling=' + this.inFormFilling);
            
            // Clear silence timer (user spoke!)
            this.clearSilenceTimer();
            this.noSpeechCount = 0; // Reset no-speech counter
            
            // STRICT: Filter low confidence (prevent false positives)
            if (confidence < 0.55) {
                console.log('⚠️ Low confidence (' + confidence + '), ignoring');
                
                // In conversation, this might be silence
                if (this.inConversation || this.inFormFilling) {
                    this.handleSilence();
                } else {
                    this.restartListening();
                }
                return;
            }
            
            // Filter too short
            if (transcript.length < 3) {
                console.log('⚠️ Too short (' + transcript.length + ' chars), ignoring');
                
                // In conversation, ask to repeat
                if (this.inConversation || this.inFormFilling) {
                    this.handleSilence();
                } else {
                    this.restartListening();
                }
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
                this.showError('يرجى السماح بالميكروفون', 'Please allow microphone');
            } else if (event.error === 'no-speech') {
                console.log('🔇 No speech detected');
                
                // If in conversation or form filling, this is silence
                if (this.inConversation || this.inFormFilling) {
                    this.handleSilence();
                } else {
                    // Just restart listening
                    this.restartListening();
                }
            } else {
                this.restartListening();
            }
        };
        
        this.recognition.onend = () => {
            console.log('🎤 Recognition ended');
            this.isListening = false;
            
            // Auto-restart if continuous mode
            if (this.continuousMode) {
                setTimeout(() => {
                    this.restartListening();
                }, 500);
            }
        };
    }
    
    // ═══════════════════════════════════════════════════════════
    // CONTINUOUS LISTENING
    // ═══════════════════════════════════════════════════════════
    
    async startContinuousListening() {
        console.log('👂 Starting continuous listening...');
        this.continuousMode = true;
        await this.startListening();
    }
    
    stopContinuousListening() {
        console.log('🔇 Stopping continuous listening');
        this.continuousMode = false;
        this.stopListening();
    }
    
    async restartListening() {
        if (!this.continuousMode) return;
        
        try {
            await this.recognition.start();
            
            // Start silence timer if in conversation
            if (this.inConversation || this.inFormFilling) {
                this.startSilenceTimer();
            }
        } catch (error) {
            if (error.name !== 'InvalidStateError') {
                console.error('❌ Restart error:', error);
            }
        }
    }
    
    // ═══════════════════════════════════════════════════════════
    // SILENCE DETECTION
    // ═══════════════════════════════════════════════════════════
    
    startSilenceTimer() {
        // Clear existing timer
        this.clearSilenceTimer();
        
        // Start new timer
        this.silenceTimeout = setTimeout(() => {
            console.log('⏱️ Silence timeout reached');
            this.handleSilence();
        }, this.silenceDelay);
    }
    
    clearSilenceTimer() {
        if (this.silenceTimeout) {
            clearTimeout(this.silenceTimeout);
            this.silenceTimeout = null;
        }
    }
    
    async handleSilence() {
        console.log('🔇 Handling silence...');
        
        this.noSpeechCount++;
        
        if (this.noSpeechCount >= this.maxNoSpeech) {
            // Too many silences, reset conversation
            await this.speak(
                'لم أسمع منك. سأنهي المحادثة. قل "أبشر" للبدء من جديد',
                'No response. Ending conversation. Say "Absher" to start again'
            );
            
            this.resetConversation();
            this.noSpeechCount = 0;
        } else {
            // Ask user to repeat
            if (this.inFormFilling) {
                // Send empty input to trigger re-prompt
                await this.processPageFieldInput('');
            } else {
                await this.speak(
                    'لم أسمع إجابة. هل تكرر من فضلك؟',
                    'I did not hear an answer. Could you repeat please?'
                );
                
                // Keep in conversation
                this.updateUI('active');
            }
        }
        
        // Restart listening
        this.restartListening();
    }
    
    resetConversation() {
        console.log('🔄 Resetting conversation');
        
        this.inConversation = false;
        this.inFormFilling = false;
        this.noSpeechCount = 0;
        this.clearSilenceTimer();
        this.updateUI('idle');
    }
    
    // ═══════════════════════════════════════════════════════════
    // VOICE INPUT PROCESSING
    // ═══════════════════════════════════════════════════════════
    
    async processVoiceInput(input) {
        console.log('💬 Processing:', input);
        console.log('📊 State: conversation=' + this.inConversation + ', formFilling=' + this.inFormFilling);
        
        // If on page and in form filling mode
        if (this.inFormFilling) {
            console.log('📝 Processing as form field input');
            await this.processPageFieldInput(input);
            return;
        }
        
        // Check for wake word
        if (this.detectWakeWord(input)) {
            console.log('🔔 Wake word detected!');
            await this.handleWakeWord(input);
            return;
        }
        
        // If in conversation, continue
        if (this.inConversation) {
            console.log('💬 Processing as conversation input');
            await this.processConversationInput(input);
            return;
        }
        
        // Not in conversation and no wake word
        console.log('⚠️ Not in conversation, ignoring input');
    }
    
    detectWakeWord(text) {
        const normalized = text.toLowerCase().replace(/أ|إ|آ/g, 'ا');
        
        // MORE STRICT: Must contain wake word as separate word or at start
        const wakeWords = ['ابشر', 'absher'];
        
        for (const word of wakeWords) {
            // Check if wake word is at start or as separate word
            if (normalized.startsWith(word) || normalized.includes(' ' + word)) {
                console.log('✅ Wake word found:', word);
                return true;
            }
        }
        
        console.log('❌ No wake word in:', text);
        return false;
    }
    
    async handleWakeWord(input) {
        // Remove wake word and get command
        let command = input.toLowerCase()
            .replace(/أبشر|ابشر|absher/gi, '')
            .trim();
        
        this.updateUI('active');
        
        if (!command || command.length < 2) {
            // Just wake word, no command
            this.inConversation = true; // SET BEFORE SPEAKING
            
            await this.speak(
                'نعم، كيف يمكنني مساعدتك؟',
                'Yes, how can I help you?'
            );
            
            // Keep listening state active
            this.updateUI('active');
            
            console.log('💬 Waiting for command...');
        } else {
            // Wake word + command
            await this.processCommand(command);
        }
    }
    
    async processCommand(command) {
        console.log('⚡ Processing command:', command);
        
        this.updateUI('processing');
        
        try {
            const response = await fetch('/api/voice/conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input: command,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                await this.handleAIResponse(data.response);
            } else {
                this.showError('خطأ في المعالجة', 'Processing error');
                this.updateUI('idle');
            }
            
        } catch (error) {
            console.error('❌ API Error:', error);
            this.showError('خطأ في الاتصال', 'Connection error');
            this.updateUI('idle');
        }
    }
    
    async processConversationInput(input) {
        await this.processCommand(input);
    }
    
    async handleAIResponse(response) {
        console.log('🤖 AI Response:', response);
        
        // Speak the response
        await this.speak(response.arabic, response.english);
        
        // Handle action
        if (response.action) {
            await this.executeAction(response.action);
        }
        
        // Update conversation state
        if (response.continue_conversation) {
            this.inConversation = true;
            this.updateUI('active');
        } else {
            this.inConversation = false;
            this.updateUI('idle');
        }
    }
    
    async executeAction(action) {
        console.log('⚡ Executing action:', action);
        
        if (action.type === 'navigate') {
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
                console.log('🧭 Navigating to:', url);
                
                // Stop any ongoing listening and reset state
                this.stopContinuousListening();
                this.resetConversation();
                
                // Wait a bit then navigate
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Navigate (page will auto-start workflow on load)
                window.location.href = url;
            }
        }
        else if (action.type === 'fill_field') {
            this.fillFormField(action.field, action.value);
        }
        else if (action.type === 'submit_form') {
            await this.submitForm(action.data);
        }
    }
    
    // ═══════════════════════════════════════════════════════════
    // PAGE-AWARE FORM FILLING
    // ═══════════════════════════════════════════════════════════
    
    async startPageWorkflow() {
        if (!this.currentPage) return;
        
        console.log('📋 Starting page workflow:', this.currentPage);
        
        try {
            const response = await fetch('/api/voice/page/start/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    page_name: this.currentPage
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success' && data.response) {
                console.log('✅ Page workflow started!');
                
                // Set state
                this.inFormFilling = true;
                this.onPage = true;
                this.continuousMode = true; // Keep listening
                this.currentFieldIndex = 0;
                this.currentFieldName = data.response.field || null;
                this.noSpeechCount = 0;
                
                // Speak first prompt
                await this.speak(data.response.arabic, data.response.english);
                
                // Update UI to show active
                this.updateUI('active');
                
                console.log('👂 Waiting for your response...');
                
                // Start listening for user response
                this.restartListening();
            }
            
        } catch (error) {
            console.error('❌ Page workflow error:', error);
        }
    }
    
    async processPageFieldInput(input) {
        console.log('📝 Processing field input:', input);
        console.log('📄 Current page:', this.currentPage);
        console.log('🎯 Current field index:', this.currentFieldIndex || 0);
        
        this.updateUI('processing');
        
        // Always use backend workflow API
        try {
            const response = await fetch('/api/voice/page/input/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input: input
                })
            });
            
            const data = await response.json();
            console.log('📨 API Response:', data);
            
            if (data.status === 'success') {
                const res = data.response;
                console.log('🧠 Workflow response:', res);
                
                if (res.field) {
                    this.currentFieldName = res.field;
                }
                
                // Handle action FIRST (fill field)
                if (res.action) {
                    if (res.action.type === 'fill_field') {
                        console.log('📝 Filling field from API:', res.action.field);
                        this.fillFormField(res.action.field, res.action.value);
                    } else if (res.action.type === 'submit_form') {
                        console.log('📤 Submitting form...');
                        await this.submitForm(res.action.data);
                        
                        await this.speak(res.arabic, res.english);
                        
                        this.inFormFilling = false;
                        this.updateUI('idle');
                        return;
                    }
                }
                
                await this.speak(res.arabic, res.english);
                
                if (res.continue_conversation) {
                    this.updateUI('active');
                    console.log('👂 Waiting for next field...');
                } else {
                    this.inFormFilling = false;
                    this.updateUI('idle');
                }
            }
            
        } catch (error) {
            console.error('❌ Field input error:', error);
            this.updateUI('error');
        }
    }
    
    fillFormField(fieldName, value) {
        console.log(`📝 Filling field: ${fieldName} = ${value}`);
        
        // Convert snake_case to camelCase and other variations
        const fieldVariations = [
            fieldName, // Original: id_number
            fieldName.replace(/_/g, ''), // Remove underscores: idnumber
            this.toCamelCase(fieldName), // camelCase: idNumber
            fieldName.replace(/_/g, '-'), // Kebab case: id-number
        ];
        
        // Build comprehensive selector list
        const selectors = [];
        
        // Try all field name variations
        for (const variation of fieldVariations) {
            selectors.push(
                `#${variation}`,
                `input[name="${variation}"]`,
                `input[id="${variation}"]`,
                `input[id*="${variation}"]`
            );
        }
        
        // Add common specific selectors
        selectors.push(
            '#idNumber',           // Violations page
            '#id-number',
            '#nationalId',
            '#plateNumber',       // Plate number field
            '#plate-number',
            'input[placeholder*="1234567890"]', // ID placeholder
            'input[placeholder*="ABC"]',        // Plate placeholder
        );
        
        // Try each selector
        for (const selector of selectors) {
            try {
                const field = document.querySelector(selector);
                if (field && !field.value) { // Only fill empty fields
                    console.log(`✅ Found field with selector: ${selector}`);
                    
                    // Set value
                    field.value = value;
                    
                    // Trigger all events
                    field.dispatchEvent(new Event('input', { bubbles: true }));
                    field.dispatchEvent(new Event('change', { bubbles: true }));
                    field.dispatchEvent(new Event('blur', { bubbles: true }));
                    field.dispatchEvent(new Event('focus', { bubbles: true }));
                    
                    // Strong visual feedback
                    field.style.borderColor = '#10b981';
                    field.style.borderWidth = '3px';
                    field.style.backgroundColor = '#f0fdf4';
                    field.style.transition = 'all 0.3s ease';
                    
                    setTimeout(() => {
                        field.style.borderColor = '';
                        field.style.borderWidth = '';
                        field.style.backgroundColor = '';
                    }, 3000);
                    
                    console.log('✅ Field filled successfully:', selector, 'value:', value);
                    return true;
                }
            } catch (e) {
                // Ignore selector errors, continue to next
            }
        }
        
        console.warn('⚠️ Field not found for:', fieldName);
        console.log('🔍 Trying fallback - first empty text input...');
        
        // Fallback: Find ANY empty text input
        const emptyInputs = document.querySelectorAll('input[type="text"]:not([readonly]):not([disabled])');
        for (const input of emptyInputs) {
            if (!input.value || input.value.trim() === '') {
                console.log('📝 Filling first empty input field');
                input.value = value;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                
                input.style.borderColor = '#10b981';
                input.style.borderWidth = '3px';
                input.style.backgroundColor = '#f0fdf4';
                
                setTimeout(() => {
                    input.style.borderColor = '';
                    input.style.borderWidth = '';
                    input.style.backgroundColor = '';
                }, 3000);
                
                return true;
            }
        }
        
        return false;
    }
    
    toCamelCase(str) {
        return str.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());
    }
    
    async submitForm(data) {
        console.log('📤 Submitting form with data:', data);
        
        // Fill all fields first
        for (const [key, value] of Object.entries(data)) {
            this.fillFormField(key, value);
        }
        
        // Wait a bit for fields to update
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Find and click submit button
        const submitSelectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button.submit-btn',
            'button.btn-primary',
            '.btn-submit'
        ];
        
        for (const selector of submitSelectors) {
            const button = document.querySelector(selector);
            if (button) {
                console.log('✅ Clicking submit button:', selector);
                button.click();
                return;
            }
        }
        
        // Try form submit
        const form = document.querySelector('form');
        if (form) {
            console.log('✅ Submitting form');
            form.submit();
        }
    }
    
    // ═══════════════════════════════════════════════════════════
    // SPEECH SYNTHESIS
    // ═══════════════════════════════════════════════════════════
    
    speak(arabicText, englishText = '') {
        return new Promise((resolve) => {
            this.synthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(arabicText);
            utterance.lang = 'ar-SA';
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 0.9;
            
            utterance.onend = () => {
                console.log('🔊 Speech finished');
                
                // If in conversation, show we're listening
                if (this.inConversation || this.inFormFilling) {
                    this.updateUI('listening');
                }
                
                resolve();
            };
            
            utterance.onerror = () => resolve();
            
            this.synthesis.speak(utterance);
            this.showStatus(arabicText, englishText, '🔊');
        });
    }
    
    // ═══════════════════════════════════════════════════════════
    // CONTROLS
    // ═══════════════════════════════════════════════════════════
    
    async manualActivate() {
        console.log('👆 Manual button clicked');
        
        // If on service page and not in form filling yet
        if (this.currentPage && !this.inFormFilling) {
            console.log('📋 Starting page workflow for:', this.currentPage);
            await this.startPageWorkflow();
            return;
        }
        
        // Otherwise toggle listening
        if (this.isListening) {
            this.stopListening();
        } else {
            await this.startListening();
        }
    }
    
    async startListening() {
        if (this.isListening) return;
        
        try {
            await this.recognition.start();
        } catch (error) {
            console.error('❌ Start error:', error);
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
        
        indicator.className = 'voice-mic-button';
        indicator.classList.add(`state-${state}`);
        
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
        setTimeout(() => {
            this.updateUI('idle');
        }, 2000);
    }
}

// ═══════════════════════════════════════════════════════════════
// INITIALIZE ON PAGE LOAD
// ═══════════════════════════════════════════════════════════════

let voiceAssistant = null;

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing Continuous Voice AI...');
    voiceAssistant = new AbsherContinuousVoiceAI();
    window.voiceAssistant = voiceAssistant;
    console.log('✅ Continuous Voice AI Ready!');
});

