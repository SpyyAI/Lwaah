/**
 * Lowaah - Enhanced Navigation and Interaction JavaScript
 * Handles keyboard shortcuts and accessibility features
 */

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Alt + C: Toggle Camera
    if (event.altKey && event.key === 'c') {
        event.preventDefault();
        document.getElementById('toggleCamera')?.click();
    }
    
    // Alt + S: Go to Services
    if (event.altKey && event.key === 's') {
        event.preventDefault();
        window.location.href = '/services/';
    }
    
    // Alt + V: Go to Violations
    if (event.altKey && event.key === 'v') {
        event.preventDefault();
        window.location.href = '/violations/';
    }
    
    // Alt + H: Go to Home
    if (event.altKey && event.key === 'h') {
        event.preventDefault();
        window.location.href = '/';
    }
    
    // Escape: Close camera panel
    if (event.key === 'Escape') {
        const cameraPanel = document.getElementById('cameraPanel');
        if (cameraPanel && cameraPanel.classList.contains('active')) {
            cameraPanel.classList.remove('active');
            if (typeof stopCamera === 'function') {
                stopCamera();
            }
        }
    }
});

// Add hover effects to service cards
document.addEventListener('DOMContentLoaded', function() {
    const serviceCards = document.querySelectorAll('.service-card, .action-card, .category-card');
    
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Show loading indicator for page transitions
let isNavigating = false;
document.querySelectorAll('a:not([href^="#"])').forEach(link => {
    link.addEventListener('click', function(e) {
        if (isNavigating) return;
        if (this.target === '_blank') return;
        if (this.href.startsWith('javascript:')) return;
        
        const href = this.getAttribute('href');
        if (!href || href === '#') return;
        
        // Show loading
        isNavigating = true;
        showLoadingIndicator();
    });
});

function showLoadingIndicator() {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
        ">
            <div style="text-align: center;">
                <div style="
                    width: 50px;
                    height: 50px;
                    border: 5px solid #e0e0e0;
                    border-top-color: #006837;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                "></div>
                <p style="margin-top: 1rem; color: #006837; font-weight: 600;">جاري التحميل...</p>
            </div>
        </div>
        <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    `;
    document.body.appendChild(loader);
}

// Accessibility: Announce page changes for screen readers
function announcePageChange(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    announcement.style.cssText = `
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0,0,0,0);
        white-space: nowrap;
        border-width: 0;
    `;
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        announcement.remove();
    }, 1000);
}

// Log keyboard shortcuts info on load
console.log(`
╔═══════════════════════════════════════════════════════════╗
║                  LOWAAH - لواح                            ║
║         Saudi Sign Language Assistant                     ║
╠═══════════════════════════════════════════════════════════╣
║  Keyboard Shortcuts:                                      ║
║  • Alt + C : Toggle Camera                                ║
║  • Alt + H : Home                                         ║
║  • Alt + S : Services                                     ║
║  • Alt + V : Violations                                   ║
║  • Escape  : Close Camera                                 ║
╚═══════════════════════════════════════════════════════════╝
`);

