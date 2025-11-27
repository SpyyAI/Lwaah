/**
 * Absher Voice Assistant - REDESIGNED & FIXED
 * 
 * Features:
 * - Manual click-to-talk
 * - Better microphone permission handling
 * - Clear visual feedback
 * - Error messages
 * - Bilingual support
 */

class AbsherVoiceAssistant {
    constructor() {
        this.isListening = false;
        this.isActive = false;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.currentLanguage = 'ar-SA';
        this.wakeWords = ['أبشر', 'ابشر', 'absher'];
        this.isProcessing = false;
        this.hasPermission = false;
        this.manualMode = false; // Click-to-talk mode
        
        this.init();
    }

    async init() {
        console.log('🎤 Initializing Voice Assistant...');
        
        // Check browser support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('متصفحك لا يدعم التعرف على الصوت. استخدم Chrome أو Edge', 
                          'Your browser does not support speech recognition. Use Chrome or Edge');
            return;
        }

        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure recognition - OPTIMIZED FOR NOISE REDUCTION
        this.recognition.continuous = false; // Single command mode
        this.recognition.interimResults = false; // Only final results
        this.recognition.lang = 'ar-SA';
        this.recognition.maxAlternatives = 1; // Only best match to avoid confusion

        // Set up event listeners
        this.setupRecognitionListeners();
        
        // Update UI
        this.updateUI('idle');
        
        console.log('✅ Voice Assistant initialized');
        
        // Show welcome message
        this.showStatus('انقر على زر المايكروفون للبدء', 'Click the microphone button to start', 'ℹ️');
    }

    setupRecognitionListeners() {
        this.recognition.onstart = () => {
            console.log('🎤 Voice recognition started');
            this.isListening = true;
            this.hasPermission = true;
            this.updateUI('listening');
            this.showStatus('أستمع...', 'Listening...', '👂');
        };

        this.recognition.onresult = (event) => {
            const results = event.results[event.results.length - 1];
            const transcript = results[0].transcript.trim().toLowerCase();
            const confidence = results[0].confidence;
            
            console.log('🗣️ Heard:', transcript, '(confidence:', confidence, ')');
            
            // FILTER OUT LOW CONFIDENCE / NOISE
            if (confidence < 0.5) {
                console.log('⚠️ Low confidence, ignoring:', confidence);
                this.showStatus('لم أسمع بوضوح. حاول مرة أخرى', 'Not clear. Try again', '🔇');
                this.updateUI('idle');
                return;
            }
            
            // FILTER OUT TOO SHORT (likely noise)
            if (transcript.length < 3) {
                console.log('⚠️ Too short, ignoring:', transcript);
                this.updateUI('idle');
                return;
            }
            
            // STOP SPEECH SYNTHESIS to prevent echo
            this.synthesis.cancel();
            
            this.showStatus(`سمعت: ${transcript}`, `Heard: ${transcript}`, '✅');
            
            if (this.manualMode) {
                // In manual mode, process any command directly
                this.processCommand(transcript);
            } else {
                // In wake word mode, check for wake word first
                if (!this.isActive) {
                    if (this.detectWakeWord(transcript)) {
                        this.activate();
                    } else {
                        this.showStatus('قل "أبشر" للبدء', 'Say "Absher" to start', 'ℹ️');
                        setTimeout(() => this.startListening(), 1000);
                    }
                } else {
                    this.processCommand(transcript);
                }
            }
        };

        this.recognition.onerror = (event) => {
            console.error('❌ Voice recognition error:', event.error);
            this.isListening = false;
            
            switch(event.error) {
                case 'not-allowed':
                case 'service-not-allowed':
                    this.showError('الرجاء السماح باستخدام المايكروفون', 'Please allow microphone access');
                    this.showPermissionBanner();
                    break;
                case 'no-speech':
                    this.showStatus('لم أسمع شيئاً. حاول مرة أخرى', 'No speech detected. Try again', '🔇');
                    if (this.manualMode) {
                        this.updateUI('idle');
                    } else {
                        setTimeout(() => this.startListening(), 1000);
                    }
                    break;
                case 'audio-capture':
                    this.showError('لا يمكن الوصول للمايكروفون. تحقق من الإعدادات', 'Cannot access microphone. Check settings');
                    break;
                case 'network':
                    this.showError('خطأ في الاتصال', 'Network error');
                    break;
                default:
                    this.showError(`خطأ: ${event.error}`, `Error: ${event.error}`);
            }
            
            this.updateUI('error');
        };

        this.recognition.onend = () => {
            console.log('🎤 Voice recognition ended');
            this.isListening = false;
            
            // In wake word mode, restart automatically
            if (!this.manualMode && this.hasPermission) {
                setTimeout(() => {
                    if (!this.isListening) {
                        this.startListening();
                    }
                }, 500);
            } else if (this.manualMode) {
                this.updateUI('idle');
            }
        };
    }

    startListening() {
        if (this.isListening) return;
        
        try {
            this.recognition.start();
            console.log('👂 Started listening...');
        } catch (e) {
            console.error('Failed to start recognition:', e);
            // Already running, ignore
        }
    }

    stopListening() {
        if (!this.isListening) return;
        
        try {
            this.recognition.stop();
            console.log('🛑 Stopped listening');
        } catch (e) {
            console.error('Failed to stop recognition:', e);
        }
    }

    detectWakeWord(transcript) {
        return this.wakeWords.some(word => transcript.includes(word));
    }

    activate() {
        this.isActive = true;
        this.updateUI('active');
        this.speak(
            'نعم، كيف يمكنني مساعدتك؟',
            'Yes, how can I help you?'
        );
    }

    deactivate() {
        this.isActive = false;
        this.isProcessing = false;
        this.updateUI('idle');
        this.speak('تم. قل "أبشر" عند الحاجة', 'Done. Say "Absher" when needed');
    }

    async processCommand(command) {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.updateUI('processing');
        
        // Normalize command
        const normalizedCommand = this.normalizeArabic(command);
        
        // Match command to intent
        const intent = this.matchIntent(normalizedCommand);
        
        if (intent) {
            await this.executeIntent(intent);
        } else {
            this.speak(
                'عذراً، لم أفهم. انقر المساعدة للخيارات',
                'Sorry, I did not understand. Click help for options'
            );
            this.showStatus('لم أفهم الأمر', 'Command not understood', '❓');
        }
        
        this.isProcessing = false;
        
        if (this.manualMode) {
            this.updateUI('idle');
        } else {
            this.updateUI('active');
        }
    }

    normalizeArabic(text) {
        return text
            .replace(/آ|إ|أ/g, 'ا')
            .replace(/ى/g, 'ي')
            .replace(/ة/g, 'ه')
            .replace(/ـ/g, '');
    }

    matchIntent(command) {
        const intents = {
            'id_renewal': ['تجديد الهوية', 'تجديد الهويه', 'تجديد بطاقة الهوية', 'الهوية', 'renew id', 'id renewal', 'identity'],
            'violations': ['المخالفات', 'مخالفات', 'الاستعلام عن المخالفات', 'violations', 'fines', 'traffic'],
            'passport': ['جواز السفر', 'الجواز', 'جواز', 'passport'],
            'driving_license': ['رخصة القيادة', 'الرخصة', 'رخصه', 'driving', 'license', 'licence'],
            'vehicle_registration': ['تسجيل المركبة', 'تسجيل السيارة', 'استمارة', 'vehicle', 'car registration'],
            'employment': ['التوظيف', 'العمل', 'وظيفة', 'employment', 'job', 'work'],
            'health': ['الصحة', 'حجز موعد', 'موعد', 'المستشفى', 'health', 'appointment', 'hospital'],
            'education': ['التعليم', 'الشهادات', 'الجامعة', 'education', 'certificate', 'university'],
            'help': ['مساعدة', 'مساعده', 'الخيارات', 'ماذا', 'help', 'options', 'what'],
            'cancel': ['إلغاء', 'الغاء', 'توقف', 'cancel', 'stop', 'quit'],
            'services': ['الخدمات', 'جميع الخدمات', 'services'],
            'home': ['الرئيسية', 'البداية', 'home', 'main']
        };

        for (const [intent, keywords] of Object.entries(intents)) {
            if (keywords.some(keyword => command.includes(keyword))) {
                return intent;
            }
        }

        return null;
    }

    async executeIntent(intent) {
        console.log('🎯 Executing intent:', intent);

        const routes = {
            'id_renewal': ['/id-renewal/', 'تجديد الهوية', 'ID renewal'],
            'violations': ['/violations/', 'المخالفات', 'Violations'],
            'passport': ['/passport/', 'جواز السفر', 'Passport'],
            'driving_license': ['/driving-license/', 'رخصة القيادة', 'Driving license'],
            'vehicle_registration': ['/vehicle-registration/', 'تسجيل المركبات', 'Vehicle registration'],
            'employment': ['/employment/', 'التوظيف', 'Employment'],
            'health': ['/health/', 'الخدمات الصحية', 'Health services'],
            'education': ['/education/', 'التعليم', 'Education']
        };

        if (intent === 'help') {
            this.toggleHelpPanel();
            this.speak('هذه هي الأوامر المتاحة', 'Here are the available commands');
            return;
        }

        if (intent === 'cancel') {
            this.deactivate();
            return;
        }

        if (intent === 'services') {
            this.speak('الخدمات', 'Services');
            await this.wait(1000);
            window.location.href = '/services/';
            return;
        }

        if (intent === 'home') {
            this.speak('الصفحة الرئيسية', 'Homepage');
            await this.wait(1000);
            window.location.href = '/';
            return;
        }

        if (routes[intent]) {
            const [url, arName, enName] = routes[intent];
            this.speak(`جاري فتح ${arName}`, `Opening ${enName}`);
            this.showStatus(`انتقال إلى ${arName}`, `Navigating to ${enName}`, '➡️');
            await this.wait(1500);
            window.location.href = url;
        }
    }

    speak(arabicText, englishText = '') {
        // STOP listening to prevent echo
        if (this.isListening) {
            this.stopListening();
        }
        
        // Cancel any ongoing speech
        this.synthesis.cancel();

        const arabicUtterance = new SpeechSynthesisUtterance(arabicText);
        arabicUtterance.lang = 'ar-SA';
        arabicUtterance.rate = 0.9; // Slower for clarity
        arabicUtterance.pitch = 1.0;
        arabicUtterance.volume = 0.9; // Slightly lower to reduce feedback

        const voices = this.synthesis.getVoices();
        const arabicVoice = voices.find(voice => voice.lang.startsWith('ar'));
        if (arabicVoice) {
            arabicUtterance.voice = arabicVoice;
        }

        this.synthesis.speak(arabicUtterance);

        // ONLY speak English if explicitly needed (reduce noise)
        if (englishText && !this.manualMode) {
            arabicUtterance.onend = () => {
                const englishUtterance = new SpeechSynthesisUtterance(englishText);
                englishUtterance.lang = 'en-US';
                englishUtterance.rate = 0.9;
                englishUtterance.volume = 0.7;
                this.synthesis.speak(englishUtterance);
            };
        }

        console.log('🔊 Speaking:', arabicText);
    }

    updateUI(state) {
        const indicator = document.getElementById('voiceIndicator');
        if (!indicator) return;

        // Update button state classes
        indicator.className = 'voice-mic-button';
        indicator.classList.add(`state-${state}`);

        // Update status badge text
        const statusTexts = {
            'idle': this.manualMode ? 'جاهز' : 'قل "أبشر"',
            'listening': 'أستمع...',
            'active': 'نشط',
            'processing': 'معالجة...',
            'error': 'خطأ'
        };

        const statusElement = indicator.querySelector('.voice-status-badge');
        if (statusElement) {
            statusElement.textContent = statusTexts[state] || 'استعداد';
        }

        // Show/hide waveform overlay
        const waveform = document.getElementById('voiceWaveform');
        if (waveform) {
            if (state === 'listening') {
                waveform.classList.add('show');
            } else {
                waveform.classList.remove('show');
            }
        }
    }

    showStatus(arabicText, englishText, icon = 'ℹ️') {
        const statusEl = document.getElementById('voiceStatusMessage');
        if (!statusEl) return;

        statusEl.innerHTML = `
            <span class="status-icon">${icon}</span>
            <div>
                <div>${arabicText}</div>
                <div style="font-size: 12px; opacity: 0.8; margin-top: 5px;">${englishText}</div>
            </div>
        `;
        statusEl.classList.add('show');

        setTimeout(() => {
            statusEl.classList.remove('show');
        }, 3000);
    }

    showError(arabicText, englishText) {
        this.showStatus(arabicText, englishText, '❌');
        this.updateUI('error');
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

    async requestPermission() {
        try {
            this.showStatus('جاري طلب الإذن...', 'Requesting permission...', '🔐');
            await navigator.mediaDevices.getUserMedia({ audio: true });
            this.hasPermission = true;
            this.hidePermissionBanner();
            this.showStatus('تم! يمكنك الآن استخدام الصوت', 'Done! You can now use voice', '✅');
            this.startListening();
        } catch (err) {
            console.error('Permission denied:', err);
            this.showError('تم رفض الإذن. افتح إعدادات المتصفح', 'Permission denied. Open browser settings');
        }
    }

    toggleManualMode() {
        this.manualMode = !this.manualMode;
        
        if (this.manualMode) {
            this.stopListening();
            this.showStatus('وضع النقر للتحدث مفعّل', 'Click-to-talk mode enabled', '🎤');
            this.updateUI('idle');
        } else {
            this.showStatus('وضع "أبشر" مفعّل', 'Wake word mode enabled', '🎤');
            if (this.hasPermission) {
                this.startListening();
            }
        }
    }

    toggleHelpPanel() {
        const panel = document.getElementById('voiceHelpPanel');
        if (panel) {
            panel.classList.toggle('show');
        }
    }

    manualActivate() {
        if (!this.hasPermission) {
            this.requestPermission();
            return;
        }

        if (this.isListening) {
            this.stopListening();
        } else {
            this.manualMode = true;
            this.isActive = true;
            this.startListening();
        }
    }

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    destroy() {
        this.isActive = false;
        this.isListening = false;
        if (this.recognition) {
            this.recognition.stop();
        }
        this.synthesis.cancel();
        console.log('🛑 Voice assistant destroyed');
    }
}

// Initialize
let voiceAssistant = null;

document.addEventListener('DOMContentLoaded', function() {
    if (speechSynthesis.getVoices().length === 0) {
        speechSynthesis.onvoiceschanged = initVoiceAssistant;
    } else {
        initVoiceAssistant();
    }
});

function initVoiceAssistant() {
    try {
        voiceAssistant = new AbsherVoiceAssistant();
        window.voiceAssistant = voiceAssistant;
        console.log('✅ Voice assistant ready');
    } catch (error) {
        console.error('❌ Failed to initialize:', error);
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AbsherVoiceAssistant;
}
