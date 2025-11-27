/**
 * Lowaah - Camera and Gesture Detection JavaScript
 * Handles webcam capture, frame processing, and gesture-based navigation
 */

// Configuration
const CONFIG = {
    CAPTURE_INTERVAL: 600, // milliseconds between captures
    CONFIDENCE_THRESHOLD: 0.5, // Lowered from 0.6 for easier detection
    API_ENDPOINT: '/api/detect-gesture/',
    MAX_WIDTH: 640,
    MAX_HEIGHT: 480,
};

// State
let videoStream = null;
let captureInterval = null;
let isCapturing = false;
let lastGesture = null;
let gestureCounter = {};
let consecutiveCount = 0;
let isFirstCapture = true;  // Track if this is the first capture after opening camera

// DOM Elements - initialized after DOM loads
let webcamElement;
let canvasElement;
let gestureValueElement;
let confidenceFillElement;
let confidenceTextElement;
let cameraPanelElement;
let toggleCameraBtn;
let closeCameraPanelBtn;

// ============================================================================
// UNIVERSAL GESTURE SYSTEM - NO CONFLICTS!
// Each gesture has ONE meaning across the entire application
// ============================================================================

const GESTURE_ACTIONS = {
    // === NAVIGATION GESTURES (Universal) ===
    'open_hand': {
        url: '/services/',
        description: '🖐️ الخدمات - Go to Services'
    },
    'closed_fist': {
        url: '/violations/',
        description: '🤘 المخالفات - Open Violations (Rock Sign)'
    },
    'victory_sign': {
        url: '/absher-individuals/',
        description: '✌️ أبشر أفراد - Go to Absher'
    },
    
    // === ACTION GESTURES (Universal) ===
    'thumbs_up': {
        action: 'next',
        description: '👍 التالي - Next/Submit'
    },
    'thumbs_down': {
        action: 'back',
        description: '👎 رجوع - Back/Cancel'
    },
    'pointing_index': {
        action: 'select',
        description: '☝️ تحديد - Select Card'
    },
    
    // === MENU NAVIGATION (Universal) ===
    'swipe_right': {
        action: 'navigate_right',
        description: '👉 التالي - Navigate Right'
    },
    'swipe_left': {
        action: 'navigate_left',
        description: '👈 السابق - Navigate Left'
    },
    
    // === UTILITY GESTURES (Universal) ===
    'ok_sign': {
        url: '/profile/setup/',
        description: '👌 الملف الشخصي - Profile Setup'
    },
    'three_fingers': {
        url: '/gesture-help/',
        description: '🖖 المساعدة - Show Settings/Help'
    }
};

/**
 * Initialize the camera and gesture detection system
 */
async function initializeCamera() {
    try {
        // Request webcam access
        videoStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: CONFIG.MAX_WIDTH },
                height: { ideal: CONFIG.MAX_HEIGHT },
                facingMode: 'user'
            }
        });

        // Set video source
        webcamElement.srcObject = videoStream;
        
        // Wait for video to be ready
        await new Promise((resolve) => {
            webcamElement.onloadedmetadata = () => {
                webcamElement.play();
                resolve();
            };
        });

        // Setup canvas
        canvasElement.width = webcamElement.videoWidth;
        canvasElement.height = webcamElement.videoHeight;

        console.log('✅ Camera initialized successfully');
        return true;

    } catch (error) {
        console.error('❌ Camera initialization failed:', error);
        alert('تعذر الوصول إلى الكاميرا. الرجاء التأكد من الأذونات.\nCannot access camera. Please check permissions.');
        return false;
    }
}

/**
 * Stop the camera and cleanup
 */
function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        videoStream = null;
    }
    
    if (captureInterval) {
        clearInterval(captureInterval);
        captureInterval = null;
    }
    
    // ⚠️ CRITICAL: Clear all gesture state when camera is stopped
    lastGesture = null;
    gestureCounter = {};
    consecutiveCount = 0;
    isFirstCapture = true;  // Reset for next session
    
    isCapturing = false;
    console.log('🛑 Camera stopped and all gesture state cleared for next session');
}

/**
 * Capture a frame from the video and convert to base64
 */
function captureFrame() {
    if (!webcamElement || !canvasElement) return null;

    const context = canvasElement.getContext('2d');
    context.drawImage(webcamElement, 0, 0, canvasElement.width, canvasElement.height);
    
    // Convert to base64 (JPEG for better performance)
    const frameData = canvasElement.toDataURL('image/jpeg', 0.8);
    return frameData;
}

/**
 * Send frame to backend for gesture detection
 */
async function detectGesture(frameData, clearBuffer = false) {
    try {
        const response = await fetch(CONFIG.API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                frame: frameData,
                clear_buffer: clearBuffer  // Clear buffer for fresh detection
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error('❌ Gesture detection error:', error);
        return { gesture: null, confidence: 0, success: false };
    }
}

/**
 * Update UI with detected gesture
 * Can be overridden by pages for custom display
 */
function updateGestureDisplay(gesture, confidence) {
    // Check if page has custom display function
    if (window.customUpdateGestureDisplay && typeof window.customUpdateGestureDisplay === 'function') {
        window.customUpdateGestureDisplay(gesture, confidence);
        updateConfidenceBar(confidence);
        return;
    }

    // Default behavior
    if (gesture && confidence >= CONFIG.CONFIDENCE_THRESHOLD) {
        const gestureInfo = GESTURE_ACTIONS[gesture];
        
        if (gestureInfo) {
            gestureValueElement.textContent = gestureInfo.description || gesture;
            gestureValueElement.style.color = 'var(--primary-green)';
        } else {
            gestureValueElement.textContent = gesture;
            gestureValueElement.style.color = 'var(--text-secondary)';
        }
        
    } else {
        gestureValueElement.textContent = 'جاري البحث عن إيماءات...';
        gestureValueElement.style.color = 'var(--text-secondary)';
    }

    updateConfidenceBar(confidence);
}

/**
 * Update confidence bar
 */
function updateConfidenceBar(confidence) {
    const confidencePercent = Math.round(confidence * 100);
    confidenceFillElement.style.width = `${confidencePercent}%`;
    confidenceTextElement.textContent = `${confidencePercent}%`;
    
    // Color based on confidence level
    if (confidence >= 0.8) {
        confidenceFillElement.style.background = 'var(--success-green)';
    } else if (confidence >= 0.6) {
        confidenceFillElement.style.background = 'var(--warning-orange)';
    } else if (confidence > 0) {
        confidenceFillElement.style.background = 'var(--danger-red)';
    } else {
        confidenceFillElement.style.width = '0%';
        confidenceTextElement.textContent = '0%';
    }
}

/**
 * Execute action based on detected gesture
 */
function executeGestureAction(gesture, confidence) {
    // Only execute if confidence is high enough
    if (confidence < CONFIG.CONFIDENCE_THRESHOLD) {
        console.log(`[GESTURE] Low confidence: ${gesture} (${confidence.toFixed(2)})`);
        return;
    }

    // Count consecutive detections to avoid false positives
    if (gesture === lastGesture) {
        consecutiveCount++;
    } else {
        consecutiveCount = 1;
        lastGesture = gesture;
    }

    console.log(`[GESTURE] Detected: ${gesture} (${consecutiveCount}/2 consecutive, conf: ${confidence.toFixed(2)})`);

    // Require 2 consecutive detections before acting
    if (consecutiveCount < 2) return;

    // Check cooldown (don't navigate too frequently)
    const now = Date.now();
    if (gestureCounter[gesture] && (now - gestureCounter[gesture]) < 3000) {
        return; // 3 second cooldown
    }
    gestureCounter[gesture] = now;

    // ============================================================================
    // CHECK FOR PAGE-SPECIFIC GESTURE CONTEXT FIRST
    // ============================================================================
    if (window.currentGestureContext && typeof window.currentGestureContext[gesture] === 'function') {
        console.log(`🎯 Page-specific action for: ${gesture}`);
        window.currentGestureContext[gesture]();
        return; // Stop here, don't execute universal action
    }

    // ============================================================================
    // FALL BACK TO UNIVERSAL GESTURES
    // ============================================================================
    const action = GESTURE_ACTIONS[gesture];
    
    if (!action) {
        console.log(`⚠️ No action defined for gesture: ${gesture}`);
        return;
    }

    // Execute action
    if (action.url) {
        console.log(`🎯 Navigating to: ${action.url}`);
        showNavigationNotification(action.description);
        setTimeout(() => {
            window.location.href = action.url;
        }, 1000);
        
    } else if (action.action) {
        console.log(`🎯 Action: ${action.action}`, action.value || '');
        handleCustomAction(action.action, action.value);
    }
}

/**
 * Show navigation notification
 */
function showNavigationNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'gesture-notification';
    notification.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    notification.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--primary-green);
        color: white;
        padding: 2rem 3rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        z-index: 10000;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: fadeInOut 1s ease-in-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 1500);
}

// Track currently focused input
let currentInput = null;
let currentInputIndex = -1;
let allInputs = [];

// Initialize input tracking
function initializeInputTracking() {
    allInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"], input[type="tel"], textarea'));
    if (allInputs.length > 0) {
        currentInputIndex = 0;
        currentInput = allInputs[0];
        focusInput(currentInput);
    }
}

function focusInput(input) {
    if (input) {
        input.focus();
        input.style.outline = '3px solid #00a859';
        input.style.outlineOffset = '2px';
    }
}

function blurInput(input) {
    if (input) {
        input.style.outline = '';
        input.style.outlineOffset = '';
    }
}

/**
 * Handle custom actions (thumbs up, select, etc.)
 */
function handleCustomAction(action, value = null) {
    switch (action) {
        case 'next':
            // Move to next input or submit form
            if (allInputs.length === 0) {
                initializeInputTracking();
            }
            
            if (currentInputIndex < allInputs.length - 1) {
                // Move to next input
                blurInput(currentInput);
                currentInputIndex++;
                currentInput = allInputs[currentInputIndex];
                focusInput(currentInput);
                showNavigationNotification(`→ الحقل التالي - Next Field (${currentInputIndex + 1}/${allInputs.length})`);
            } else {
                // Submit form
                const submitButton = document.querySelector('button[type="submit"], .btn-primary');
                if (submitButton) {
                    showNavigationNotification('✓ إرسال - Submitting Form');
                    setTimeout(() => submitButton.click(), 1000);
                }
            }
            break;
            
        case 'back':
            // Move to previous input or go back
            if (currentInputIndex > 0) {
                blurInput(currentInput);
                currentInputIndex--;
                currentInput = allInputs[currentInputIndex];
                focusInput(currentInput);
                showNavigationNotification(`← الحقل السابق - Previous Field (${currentInputIndex + 1}/${allInputs.length})`);
            } else {
                showNavigationNotification('← رجوع - Going Back');
                setTimeout(() => window.history.back(), 1000);
            }
            break;
            
        case 'select':
            // Focus on first input or select element
            if (allInputs.length === 0) {
                initializeInputTracking();
            }
            
            if (currentInput) {
                focusInput(currentInput);
                showNavigationNotification('✓ تحديد الحقل - Field Selected');
            } else {
                // Select first card if no inputs
                const firstCard = document.querySelector('.service-card, .action-card');
                if (firstCard) {
                    firstCard.style.transform = 'scale(1.05)';
                    firstCard.style.boxShadow = '0 8px 24px rgba(0,104,55,0.3)';
                    setTimeout(() => {
                        firstCard.style.transform = '';
                        firstCard.style.boxShadow = '';
                    }, 1000);
                }
            }
            break;
        
        case 'backspace':
            // Delete last character from current field
            if (!currentInput && allInputs.length > 0) {
                currentInput = allInputs[0];
                currentInputIndex = 0;
                focusInput(currentInput);
            }
            
            if (currentInput && currentInput.value.length > 0) {
                currentInput.value = currentInput.value.slice(0, -1);
                showNavigationNotification('⌫ حذف - Deleted');
                
                // Trigger input event
                currentInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            break;
            
        case 'navigate_right':
        case 'navigate_left':
            // Scroll horizontally if applicable
            const container = document.querySelector('.services-grid, .actions-grid');
            if (container) {
                const scrollAmount = action === 'navigate_right' ? 300 : -300;
                container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            }
            break;
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    initializeInputTracking();
});

/**
 * Main capture loop
 */
async function captureLoop() {
    if (!isCapturing) return;

    const frameData = captureFrame();
    if (!frameData) {
        console.log('[CAMERA] Failed to capture frame');
        return;
    }

    // Clear buffer on first capture after opening camera for fresh detection
    const result = await detectGesture(frameData, isFirstCapture);
    
    // Reset first capture flag after first detection
    if (isFirstCapture) {
        isFirstCapture = false;
        console.log('[CAMERA] Buffer cleared for fresh detection session');
    }
    
    console.log('[API] Response:', result);
    
    if (result.success && result.gesture) {
        console.log(`[DETECTION] Gesture: ${result.gesture}, Confidence: ${result.confidence.toFixed(2)}`);
        updateGestureDisplay(result.gesture, result.confidence);
        executeGestureAction(result.gesture, result.confidence);
    } else {
        updateGestureDisplay(null, 0);
    }
}

/**
 * Start gesture detection
 */
async function startGestureDetection() {
    const initialized = await initializeCamera();
    if (!initialized) return;

    // ⚠️ CRITICAL: Reset first capture flag to clear buffer on new session
    isFirstCapture = true;
    
    isCapturing = true;
    captureInterval = setInterval(captureLoop, CONFIG.CAPTURE_INTERVAL);
    console.log('🎥 Gesture detection started - Buffer will be cleared on first capture');
}

/**
 * Toggle camera panel
 */
async function toggleCameraPanel() {
    const isActive = cameraPanelElement.classList.toggle('active');
    
    if (isActive) {
        await startGestureDetection();
    } else {
        stopCamera();
    }
}

/**
 * Initialize DOM elements and event listeners
 */
function initializeCameraSystem() {
    // Initialize DOM Elements
    webcamElement = document.getElementById('webcam');
    canvasElement = document.getElementById('canvas');
    gestureValueElement = document.getElementById('gestureValue');
    confidenceFillElement = document.getElementById('confidenceFill');
    confidenceTextElement = document.getElementById('confidenceText');
    cameraPanelElement = document.getElementById('cameraPanel');
    toggleCameraBtn = document.getElementById('toggleCamera');
    closeCameraPanelBtn = document.getElementById('closeCameraPanel');
    
    // Event Listeners
    if (toggleCameraBtn) {
        toggleCameraBtn.addEventListener('click', toggleCameraPanel);
        console.log('✅ Camera button initialized');
    } else {
        console.error('❌ Camera button not found');
    }

    if (closeCameraPanelBtn) {
        closeCameraPanelBtn.addEventListener('click', () => {
            cameraPanelElement.classList.remove('active');
            stopCamera();
        });
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCameraSystem);
} else {
    // DOM is already ready
    initializeCameraSystem();
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopCamera();
});

// Add CSS animation for notification (wrapped in IIFE to avoid global conflicts)
(function() {
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        @keyframes fadeInOut {
            0% {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.8);
            }
            20% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            80% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            100% {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.8);
            }
        }
    `;
    document.head.appendChild(styleElement);
})();

console.log('✅ Lowaah Camera System Ready');

