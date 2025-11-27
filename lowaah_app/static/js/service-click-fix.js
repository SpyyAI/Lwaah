/**
 * Service Card Click Fix
 * Ensures all service cards are clickable
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Service click fix loaded');
    
    // Make entire service card clickable
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        // Make the whole card clickable
        card.style.cursor = 'pointer';
        
        card.addEventListener('click', function(e) {
            // Find the link inside the card
            const link = this.querySelector('.btn-service');
            
            if (link && !e.target.closest('.btn-service')) {
                console.log('🖱️ Card clicked, navigating to:', link.href);
                window.location.href = link.href;
            }
        });
        
        // Ensure button clicks work
        const button = card.querySelector('.btn-service');
        if (button) {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                console.log('🔘 Button clicked, navigating to:', this.href);
            });
        }
    });
    
    console.log(`✅ Fixed ${serviceCards.length} service cards`);
});


