/**
 * Common Utility Functions
 * 
 * Reusable utilities across the application.
 */

const Utils = {
    /**
     * Auto-hide flash messages after a delay
     * @param {string} elementId - ID of the messages container
     * @param {number} delay - Delay in milliseconds before hiding (default: 5000)
     */
    autoHideMessages: function(elementId = 'messages', delay = 5000) {
        setTimeout(function() {
            const messagesEl = document.getElementById(elementId);
            if (messagesEl) {
                messagesEl.style.opacity = '0';
                messagesEl.style.transition = 'opacity 0.5s';
                setTimeout(() => messagesEl.remove(), 500);
            }
        }, delay);
    },

    /**
     * Initialize auto-hide for flash messages on page load
     */
    initAutoHideMessages: function() {
        this.autoHideMessages();
    }
};

// Initialize utilities when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    Utils.initAutoHideMessages();
});

// Expose globally
window.Utils = Utils;
