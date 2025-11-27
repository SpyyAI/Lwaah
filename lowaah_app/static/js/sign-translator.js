/**
 * Sign Language Translation Interface
 * Main controller for sign-to-text and text-to-sign translation
 * 
 * Features:
 * - Real-time sign recognition
 * - Intent understanding
 * - Service navigation
 * - Text-to-sign output with avatar
 */

class SignLanguageTranslator {
    constructor() {
        // Translation state
        this.recognizedText = '';
        this.currentIntent = null;
        this.isTranslating = false;
        
        // Video stream
        this.stream = null;
        this.videoElement = null;
        this.canvas = null;
        this.ctx = null;
        
        // Avatar
        this.avatar = null;
        
        // Frame capture settings
        this.captureInterval = null;
        this.frameRate = 10; // Frames per second to process
        
        // UI elements
        this.setupUI();
        
        console.log('✅ Sign Language Translator initialized');
    }
    
    /**
     * Setup UI elements
     */
    setupUI() {
        // Create main translation panel
        this.panel = document.createElement('div');
        this.panel.id = 'sign-translation-panel';
        this.panel.className = 'sign-translation-panel hidden';
        this.panel.innerHTML = `
            <div class="translation-header">
                <h3>🤟 ترجمة لغة الإشارة - Sign Language Translation</h3>
                <button class="close-btn" onclick="signTranslator.close()">✕</button>
            </div>
            
            <div class="translation-content">
                <!-- Camera View -->
                <div class="camera-section">
                    <video id="sign-video" autoplay playsinline muted></video>
                    <canvas id="sign-canvas" style="display:none;"></canvas>
                    <div class="camera-status">
                        <span class="status-indicator">●</span>
                        <span id="camera-status-text">جاري التهيئة...</span>
                    </div>
                </div>
                
                <!-- Recognition Results -->
                <div class="recognition-section">
                    <div class="section-title">النص المترجم - Translated Text</div>
                    <div id="recognized-text" class="recognized-text">
                        <span class="placeholder">ابدأ بالإشارة...</span>
                    </div>
                    <div class="recognition-controls">
                        <button onclick="signTranslator.clearText()" class="btn-secondary">
                            🗑️ مسح - Clear
                        </button>
                        <button onclick="signTranslator.processRequest()" class="btn-primary">
                            ✅ تنفيذ - Execute
                        </button>
                    </div>
                </div>
                
                <!-- Intent & Actions -->
                <div class="intent-section" id="intent-section" style="display:none;">
                    <div class="section-title">الإجراء المقترح - Suggested Action</div>
                    <div id="intent-display" class="intent-display"></div>
                    <div id="actions-display" class="actions-display"></div>
                </div>
                
                <!-- Response Avatar -->
                <div class="response-section" id="response-section" style="display:none;">
                    <div class="section-title">استجابة النظام - System Response</div>
                    <div id="response-text" class="response-text"></div>
                    <div id="avatar-container" class="avatar-container"></div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.panel);
        
        // Add toggle button to header
        const header = document.querySelector('.header-content');
        if (header) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'header-icon';
            toggleBtn.innerHTML = '🤟';
            toggleBtn.title = 'ترجمة لغة الإشارة';
            toggleBtn.onclick = () => this.toggle();
            header.appendChild(toggleBtn);
        }
    }
    
    /**
     * Toggle translation panel
     */
    toggle() {
        if (this.panel.classList.contains('hidden')) {
            this.open();
        } else {
            this.close();
        }
    }
    
    /**
     * Open translation panel
     */
    async open() {
        this.panel.classList.remove('hidden');
        await this.startCamera();
        this.startTranslation();
    }
    
    /**
     * Close translation panel
     */
    close() {
        this.panel.classList.add('hidden');
        this.stopTranslation();
        this.stopCamera();
    }
    
    /**
     * Start camera
     */
    async startCamera() {
        try {
            this.videoElement = document.getElementById('sign-video');
            this.canvas = document.getElementById('sign-canvas');
            this.ctx = this.canvas.getContext('2d');
            
            // Request camera access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                },
                audio: false
            });
            
            this.videoElement.srcObject = this.stream;
            
            // Update status
            document.getElementById('camera-status-text').textContent = 'الكاميرا نشطة - Camera Active';
            
            // Initialize avatar
            this.initializeAvatar();
            
            console.log('✅ Camera started');
            
        } catch (error) {
            console.error('❌ Camera error:', error);
            document.getElementById('camera-status-text').textContent = 
                'خطأ في الكاميرا - Camera Error';
        }
    }
    
    /**
     * Stop camera
     */
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
    }
    
    /**
     * Initialize 3D avatar
     */
    initializeAvatar() {
        if (typeof SignLanguageAvatar !== 'undefined') {
            const container = document.getElementById('avatar-container');
            this.avatar = new SignLanguageAvatar('avatar-container');
            console.log('✅ Avatar initialized');
        } else {
            console.warn('⚠️ SignLanguageAvatar not available');
        }
    }
    
    /**
     * Start continuous translation
     */
    startTranslation() {
        if (this.isTranslating) return;
        
        this.isTranslating = true;
        
        // Capture and process frames
        this.captureInterval = setInterval(() => {
            this.captureAndProcessFrame();
        }, 1000 / this.frameRate);
        
        console.log('🎬 Translation started');
    }
    
    /**
     * Stop translation
     */
    stopTranslation() {
        this.isTranslating = false;
        
        if (this.captureInterval) {
            clearInterval(this.captureInterval);
            this.captureInterval = null;
        }
        
        console.log('⏹️ Translation stopped');
    }
    
    /**
     * Capture and process frame
     */
    async captureAndProcessFrame() {
        if (!this.videoElement || !this.isTranslating) return;
        
        // Draw video frame to canvas
        this.canvas.width = this.videoElement.videoWidth;
        this.canvas.height = this.videoElement.videoHeight;
        this.ctx.drawImage(this.videoElement, 0, 0);
        
        // Get frame as base64
        const frameData = this.canvas.toDataURL('image/jpeg', 0.8);
        
        try {
            // Send to backend for recognition
            const response = await fetch('/api/translate/sign-to-text/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ frame: frameData })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.updateRecognitionDisplay(result);
            }
            
        } catch (error) {
            console.error('Translation error:', error);
        }
    }
    
    /**
     * Update recognition display
     */
    updateRecognitionDisplay(result) {
        const textDisplay = document.getElementById('recognized-text');
        const intentSection = document.getElementById('intent-section');
        
        // Update recognized text
        if (result.recognized_text && result.recognized_text.length > 0) {
            textDisplay.innerHTML = `<span class="text-content">${result.recognized_text}</span>`;
            this.recognizedText = result.recognized_text;
        }
        
        // Show current sign being detected
        if (result.current_sign && result.status === 'detecting') {
            const confidence = (result.confidence * 100).toFixed(0);
            textDisplay.innerHTML += `
                <div class="current-sign">
                    <span class="sign-label">${result.current_sign}</span>
                    <span class="confidence">${confidence}%</span>
                </div>
            `;
        }
        
        // Update intent if available
        if (result.intent && result.intent.confidence > 0.6) {
            this.currentIntent = result.intent;
            this.displayIntent(result.intent);
            intentSection.style.display = 'block';
        }
    }
    
    /**
     * Display intent information
     */
    displayIntent(intent) {
        const intentDisplay = document.getElementById('intent-display');
        const confidence = (intent.confidence * 100).toFixed(0);
        
        intentDisplay.innerHTML = `
            <div class="intent-card">
                <div class="intent-header">
                    <span class="intent-name">${intent.text_ar}</span>
                    <span class="intent-confidence">${confidence}%</span>
                </div>
                <div class="intent-service">
                    📍 ${intent.text_en}
                </div>
            </div>
        `;
    }
    
    /**
     * Process service request
     */
    async processRequest() {
        if (!this.recognizedText) {
            alert('لا يوجد نص للمعالجة - No text to process');
            return;
        }
        
        try {
            const response = await fetch('/api/translate/process-request/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: this.recognizedText })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show response
                this.displayResponse(result);
                
                // Navigate after delay
                setTimeout(() => {
                    if (result.navigation_url) {
                        window.location.href = result.navigation_url;
                    }
                }, 3000);
            } else {
                alert('خطأ في المعالجة - Processing Error: ' + result.error);
            }
            
        } catch (error) {
            console.error('Processing error:', error);
            alert('خطأ في الاتصال - Connection Error');
        }
    }
    
    /**
     * Display system response
     */
    async displayResponse(result) {
        const responseSection = document.getElementById('response-section');
        const responseText = document.getElementById('response-text');
        
        responseSection.style.display = 'block';
        responseText.textContent = result.response_text;
        
        // Play sign language animation
        if (result.sign_animation && this.avatar) {
            try {
                const animationData = JSON.parse(result.sign_animation);
                await this.avatar.playAnimation(animationData);
            } catch (error) {
                console.error('Avatar animation error:', error);
            }
        }
        
        // Show actions
        if (result.actions && result.actions.length > 0) {
            this.displayActions(result.actions);
        }
    }
    
    /**
     * Display suggested actions
     */
    displayActions(actions) {
        const actionsDisplay = document.getElementById('actions-display');
        
        actionsDisplay.innerHTML = '<div class="actions-title">الإجراءات المتاحة:</div>';
        
        actions.forEach(action => {
            const actionBtn = document.createElement('button');
            actionBtn.className = 'action-btn';
            actionBtn.innerHTML = `${action.icon} ${action.name_ar}`;
            actionBtn.onclick = () => this.executeAction(action);
            actionsDisplay.appendChild(actionBtn);
        });
    }
    
    /**
     * Execute action
     */
    executeAction(action) {
        console.log('Executing action:', action);
        // Implement action execution logic
    }
    
    /**
     * Clear recognized text
     */
    async clearText() {
        this.recognizedText = '';
        this.currentIntent = null;
        
        // Clear UI
        document.getElementById('recognized-text').innerHTML = 
            '<span class="placeholder">ابدأ بالإشارة...</span>';
        document.getElementById('intent-section').style.display = 'none';
        document.getElementById('response-section').style.display = 'none';
        
        // Clear backend session
        try {
            await fetch('/api/translate/clear-session/', { method: 'POST' });
        } catch (error) {
            console.error('Clear session error:', error);
        }
    }
    
    /**
     * Manual text-to-sign translation
     */
    async translateTextToSign(text) {
        try {
            const response = await fetch('/api/translate/text-to-sign/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const result = await response.json();
            
            if (result.success && this.avatar) {
                const animationData = JSON.parse(result.animation_data);
                await this.avatar.playAnimation(animationData);
            }
            
            return result;
            
        } catch (error) {
            console.error('Text-to-sign error:', error);
            return { success: false, error: error.message };
        }
    }
}

// Initialize global instance
let signTranslator;

document.addEventListener('DOMContentLoaded', () => {
    signTranslator = new SignLanguageTranslator();
    console.log('✅ Sign Translator ready');
});

// Export for use in other scripts
window.SignLanguageTranslator = SignLanguageTranslator;


