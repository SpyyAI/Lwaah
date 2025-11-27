/**
 * Visual Confirmation Dialogs - Highly Visual, Icon-Based Dialogs
 * Designed for deaf/mute users with minimal text dependency
 */

class VisualDialog {
    constructor() {
        this.dialogContainer = null;
        this.createDialogContainer();
    }

    createDialogContainer() {
        if (document.getElementById('visualDialogContainer')) {
            this.dialogContainer = document.getElementById('visualDialogContainer');
            return;
        }

        this.dialogContainer = document.createElement('div');
        this.dialogContainer.id = 'visualDialogContainer';
        this.dialogContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(5px);
        `;
        document.body.appendChild(this.dialogContainer);
    }

    /**
     * Show a yes/no confirmation dialog
     * @param {Object} options - Dialog options
     * @param {string} options.icon - Large emoji icon (e.g., '💰', '🚗')
     * @param {string} options.title - Main title (Arabic)
     * @param {string} options.titleEn - English title
     * @param {string} options.message - Message text (optional)
     * @param {Function} options.onYes - Callback for yes/approve
     * @param {Function} options.onNo - Callback for no/cancel
     */
    confirm(options) {
        const {
            icon = '❓',
            title = 'تأكيد',
            titleEn = 'Confirm',
            message = '',
            onYes = () => {},
            onNo = () => {}
        } = options;

        this.dialogContainer.innerHTML = `
            <div class="visual-dialog-card" style="
                background: white;
                border-radius: 30px;
                padding: 50px;
                max-width: 600px;
                width: 90%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                animation: dialogFadeIn 0.3s ease;
            ">
                <div class="dialog-icon" style="font-size: 120px; margin-bottom: 30px;">
                    ${icon}
                </div>
                
                <h2 style="font-size: 36px; color: #1e3a8a; margin-bottom: 10px;">
                    ${title}
                </h2>
                
                <p style="font-size: 24px; color: #64748b; margin-bottom: 20px;">
                    ${titleEn}
                </p>
                
                ${message ? `<p style="font-size: 20px; color: #475569; margin-bottom: 40px;">${message}</p>` : ''}
                
                <div style="display: flex; gap: 20px; justify-content: center; margin-top: 40px;">
                    <button id="visualDialogNo" style="
                        background: linear-gradient(135deg, #64748b 0%, #475569 100%);
                        color: white;
                        border: none;
                        border-radius: 50px;
                        padding: 20px 50px;
                        font-size: 24px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: all 0.3s;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                        min-width: 180px;
                    ">
                        <div style="font-size: 32px; margin-bottom: 8px;">👎</div>
                        <div>لا - No</div>
                    </button>
                    
                    <button id="visualDialogYes" style="
                        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                        color: white;
                        border: none;
                        border-radius: 50px;
                        padding: 20px 50px;
                        font-size: 24px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: all 0.3s;
                        box-shadow: 0 5px 15px rgba(34,197,94,0.3);
                        min-width: 180px;
                    ">
                        <div style="font-size: 32px; margin-bottom: 8px;">👍</div>
                        <div>نعم - Yes</div>
                    </button>
                </div>
            </div>
        `;

        // Show dialog
        this.dialogContainer.style.display = 'flex';

        // Add event listeners
        document.getElementById('visualDialogYes').addEventListener('click', () => {
            this.close();
            onYes();
        });

        document.getElementById('visualDialogNo').addEventListener('click', () => {
            this.close();
            onNo();
        });

        // Hover effects
        document.getElementById('visualDialogYes').addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(34,197,94,0.4)';
        });
        document.getElementById('visualDialogYes').addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(34,197,94,0.3)';
        });

        document.getElementById('visualDialogNo').addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
        });
        document.getElementById('visualDialogNo').addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        });

        // Close on outside click
        this.dialogContainer.addEventListener('click', (e) => {
            if (e.target === this.dialogContainer) {
                this.close();
                onNo();
            }
        });
    }

    /**
     * Show a success message
     */
    success(options) {
        const {
            icon = '✅',
            title = 'نجح!',
            titleEn = 'Success!',
            message = '',
            autoDismiss = true,
            dismissTime = 3000,
            onClose = () => {}
        } = options;

        this.dialogContainer.innerHTML = `
            <div class="visual-dialog-card" style="
                background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                color: white;
                border-radius: 30px;
                padding: 50px;
                max-width: 500px;
                width: 90%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(34,197,94,0.4);
                animation: dialogFadeIn 0.3s ease;
            ">
                <div style="font-size: 120px; margin-bottom: 30px;">
                    ${icon}
                </div>
                
                <h2 style="font-size: 36px; margin-bottom: 10px;">
                    ${title}
                </h2>
                
                <p style="font-size: 24px; opacity: 0.9; margin-bottom: 20px;">
                    ${titleEn}
                </p>
                
                ${message ? `<p style="font-size: 20px; opacity: 0.9;">${message}</p>` : ''}
            </div>
        `;

        this.dialogContainer.style.display = 'flex';

        if (autoDismiss) {
            setTimeout(() => {
                this.close();
                onClose();
            }, dismissTime);
        }
    }

    /**
     * Show an error message
     */
    error(options) {
        const {
            icon = '❌',
            title = 'خطأ!',
            titleEn = 'Error!',
            message = '',
            autoDismiss = true,
            dismissTime = 3000,
            onClose = () => {}
        } = options;

        this.dialogContainer.innerHTML = `
            <div class="visual-dialog-card" style="
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white;
                border-radius: 30px;
                padding: 50px;
                max-width: 500px;
                width: 90%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(239,68,68,0.4);
                animation: dialogShake 0.5s ease;
            ">
                <div style="font-size: 120px; margin-bottom: 30px;">
                    ${icon}
                </div>
                
                <h2 style="font-size: 36px; margin-bottom: 10px;">
                    ${title}
                </h2>
                
                <p style="font-size: 24px; opacity: 0.9; margin-bottom: 20px;">
                    ${titleEn}
                </p>
                
                ${message ? `<p style="font-size: 20px; opacity: 0.9;">${message}</p>` : ''}
            </div>
        `;

        this.dialogContainer.style.display = 'flex';

        if (autoDismiss) {
            setTimeout(() => {
                this.close();
                onClose();
            }, dismissTime);
        }
    }

    /**
     * Show a loading/processing dialog
     */
    loading(options) {
        const {
            icon = '⏳',
            title = 'جاري المعالجة...',
            titleEn = 'Processing...',
            message = ''
        } = options;

        this.dialogContainer.innerHTML = `
            <div class="visual-dialog-card" style="
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                border-radius: 30px;
                padding: 50px;
                max-width: 500px;
                width: 90%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(59,130,246,0.4);
                animation: dialogFadeIn 0.3s ease;
            ">
                <div style="font-size: 120px; margin-bottom: 30px; animation: spin 2s linear infinite;">
                    ${icon}
                </div>
                
                <h2 style="font-size: 36px; margin-bottom: 10px;">
                    ${title}
                </h2>
                
                <p style="font-size: 24px; opacity: 0.9; margin-bottom: 20px;">
                    ${titleEn}
                </p>
                
                ${message ? `<p style="font-size: 20px; opacity: 0.9;">${message}</p>` : ''}
            </div>
        `;

        this.dialogContainer.style.display = 'flex';
    }

    /**
     * Close the dialog
     */
    close() {
        this.dialogContainer.style.display = 'none';
        this.dialogContainer.innerHTML = '';
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes dialogFadeIn {
        from {
            opacity: 0;
            transform: scale(0.8) translateY(-50px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    @keyframes dialogShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Create global instance
window.visualDialog = new VisualDialog();

