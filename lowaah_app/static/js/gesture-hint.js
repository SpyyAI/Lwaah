/**
 * Lowaah - Floating Gesture Hint System
 * Shows contextual gesture hints on pages
 */

// Configuration
const HINT_CONFIG = {
    autoShow: true,
    autoHideDelay: 10000, // 10 seconds
    position: 'bottom-right',
    showOnLoad: true
};

// Create hint HTML
function createGestureHint(gestures = []) {
    const hint = document.createElement('div');
    hint.id = 'gestureHint';
    hint.className = 'gesture-hint';
    
    let gesturesHTML = '';
    gestures.forEach(g => {
        gesturesHTML += `
            <div class="hint-gesture">
                <span class="hint-icon">${g.icon}</span>
                <span class="hint-text">${g.text}</span>
            </div>
        `;
    });
    
    hint.innerHTML = `
        <div class="hint-header">
            <span class="hint-title">
                <i class="fas fa-hand-paper"></i>
                إيماءات سريعة
            </span>
            <button class="hint-close" onclick="closeGestureHint()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="hint-content">
            ${gesturesHTML}
        </div>
        <div class="hint-footer">
            <a href="/gesture-help/" class="hint-link">
                <i class="fas fa-book"></i>
                عرض الدليل الكامل
            </a>
        </div>
    `;
    
    return hint;
}

// Add CSS for hint
function addGestureHintStyles() {
    if (document.getElementById('gestureHintStyles')) return;
    
    const style = document.createElement('style');
    style.id = 'gestureHintStyles';
    style.textContent = `
        .gesture-hint {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 30px rgba(0, 104, 55, 0.2);
            width: 320px;
            z-index: 998;
            animation: slideInRight 0.4s ease;
            border: 2px solid #006837;
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .gesture-hint.hidden {
            animation: slideOutRight 0.3s ease;
            pointer-events: none;
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
        
        .hint-header {
            background: linear-gradient(135deg, #006837 0%, #004d28 100%);
            color: white;
            padding: 1rem;
            border-radius: 13px 13px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .hint-title {
            font-weight: bold;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .hint-close {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .hint-close:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }
        
        .hint-content {
            padding: 1rem;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .hint-gesture {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            padding: 0.8rem;
            margin-bottom: 0.5rem;
            background: #f6f9fc;
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        .hint-gesture:hover {
            background: #e8f5e9;
            transform: translateX(-3px);
        }
        
        .hint-icon {
            font-size: 2rem;
            min-width: 40px;
            text-align: center;
        }
        
        .hint-text {
            font-size: 0.9rem;
            color: #333;
            line-height: 1.4;
        }
        
        .hint-footer {
            padding: 0.8rem 1rem;
            border-top: 1px solid #e0e0e0;
            text-align: center;
        }
        
        .hint-link {
            color: #006837;
            text-decoration: none;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
        }
        
        .hint-link:hover {
            color: #004d28;
            transform: scale(1.05);
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .gesture-hint {
                width: calc(100% - 40px);
                right: 20px;
                left: 20px;
                bottom: 10px;
            }
        }
    `;
    
    document.head.appendChild(style);
}

// Close hint
function closeGestureHint() {
    const hint = document.getElementById('gestureHint');
    if (hint) {
        hint.classList.add('hidden');
        setTimeout(() => hint.remove(), 300);
        
        // Store that user closed it
        sessionStorage.setItem('gestureHintClosed', 'true');
    }
}

// Show hint
function showGestureHint(gestures = []) {
    // Check if already closed this session
    if (sessionStorage.getItem('gestureHintClosed') === 'true') {
        return;
    }
    
    // Remove existing hint
    const existing = document.getElementById('gestureHint');
    if (existing) existing.remove();
    
    // Add styles
    addGestureHintStyles();
    
    // Create and add hint
    const hint = createGestureHint(gestures);
    document.body.appendChild(hint);
    
    // Auto-hide after delay
    if (HINT_CONFIG.autoHideDelay > 0) {
        setTimeout(() => {
            if (document.getElementById('gestureHint')) {
                closeGestureHint();
            }
        }, HINT_CONFIG.autoHideDelay);
    }
}

// Page-specific gestures
const PAGE_GESTURES = {
    '/': [
        { icon: '🖐️', text: 'يد مفتوحة → الخدمات<br>Open Palm → Services' },
        { icon: '🤘', text: 'إشارة الروك → المخالفات<br>Rock Sign → Violations' },
        { icon: '✌️', text: 'علامة النصر → أبشر<br>V Sign → Absher' },
        { icon: '👌', text: 'إشارة موافق → الملف الشخصي<br>OK Sign → Profile' }
    ],
    '/violations/': [
        { icon: '👍', text: 'إبهام للأعلى → التالي<br>Thumbs Up → Next Field' },
        { icon: '👎', text: 'إبهام للأسفل → رجوع<br>Thumbs Down → Previous' },
        { icon: '☝️', text: 'إصبع مشير → تحديد<br>Pointing → Select' },
        { icon: '🖐️', text: 'يد مفتوحة → الخدمات<br>Open Palm → Home' }
    ],
    '/profile/select/': [
        { icon: '☝️', text: 'إصبع مشير → الملف الأول<br>Pointing Index → Profile 1' },
        { icon: '✌️', text: 'علامة النصر → الملف الثاني<br>Victory Sign → Profile 2' },
        { icon: '🖖', text: 'ثلاثة أصابع → الملف الثالث<br>Three Fingers → Profile 3' },
        { icon: '👌', text: 'إشارة موافق → ملف جديد<br>OK Sign → New Profile' },
        { icon: '👍', text: 'إبهام للأعلى → تأكيد<br>Thumbs Up → Confirm' },
        { icon: '👎', text: 'إبهام للأسفل → رجوع<br>Thumbs Down → Back' }
    ],
    '/profile/create/': [
        { icon: '👍', text: 'إبهام للأعلى → التالي<br>Thumbs Up → Next Step' },
        { icon: '👎', text: 'إبهام للأسفل → رجوع<br>Thumbs Down → Previous' },
        { icon: '🖖', text: 'ثلاثة أصابع → مساعدة<br>Three Fingers → Help' }
    ]
};

// Auto-initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    if (!HINT_CONFIG.showOnLoad) return;
    
    // Wait a bit for page to settle
    setTimeout(() => {
        const path = window.location.pathname;
        
        // Find matching gestures
        let gestures = PAGE_GESTURES[path];
        
        // Default gestures if no specific page found
        if (!gestures) {
            gestures = [
                { icon: '👍', text: 'إبهام للأعلى → التالي<br>Thumbs Up → Next' },
                { icon: '👎', text: 'إبهام للأسفل → رجوع<br>Thumbs Down → Back' },
                { icon: '🖖', text: 'ثلاثة أصابع → مساعدة<br>Three Fingers → Help' }
            ];
        }
        
        showGestureHint(gestures);
    }, 2000); // Show after 2 seconds
});

// Make functions globally available
window.showGestureHint = showGestureHint;
window.closeGestureHint = closeGestureHint;

console.log('✅ Gesture Hint System loaded');

