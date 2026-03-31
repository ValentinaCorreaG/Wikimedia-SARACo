/**
 * Modal Management for SARA
 * 
 * Handles opening, closing, and managing modal dialogs using HTMX.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Handle modal close trigger
    document.addEventListener('htmx:afterRequest', function(event) {
        // Check if the response contains the modalClose trigger
        const triggerHeader = event.detail.xhr.getResponseHeader('HX-Trigger');
        if (!triggerHeader) return;

        try {
            const triggers = JSON.parse(triggerHeader);
            if (triggers.modalClose) {
                const { modalId, contentId, reload } = triggers.modalClose;
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.close();
                }
                
                // Reload the page if needed
                if (reload) {
                    setTimeout(() => {
                        location.reload();
                    }, 300);
                }
            }
        } catch (e) {
            console.warn('Could not parse HX-Trigger header:', triggerHeader);
        }
    });

    // Close modal when clicking the X button
    document.addEventListener('click', function(event) {
        if (event.target.closest('[data-modal-close]')) {
            const modal = event.target.closest('[data-modal-target]');
            if (modal) {
                const modalId = modal.getAttribute('data-modal-target');
                const element = document.getElementById(modalId);
                if (element) {
                    element.close();
                }
            }
        }
    });

    // Close modal when pressing Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const modals = document.querySelectorAll('dialog[open]');
            modals.forEach(modal => {
                modal.close();
            });
        }
    });
});

/**
 * Open a modal dialog with HTMX content
 * @param {string} modalId - The ID of the modal dialog element
 * @param {string} contentId - The ID of the modal content container
 * @param {string} url - The URL to fetch the content from
 * @param {string} swapMode - HTMX swap mode (default: 'innerHTML')
 */
function openModal(modalId, contentId, url, swapMode = 'innerHTML') {
    const modal = document.getElementById(modalId);
    const content = document.getElementById(contentId);
    
    if (!modal || !content) {
        console.warn('Modal or content element not found');
        return;
    }

    // Load content via HTMX
    htmx.ajax('GET', url, {
        target: contentId,
        swap: swapMode,
        onError: function(error) {
            console.error('Error loading modal content:', error);
            content.innerHTML = '<div class="alert alert-error">Error loading content</div>';
        },
        onLoad: function() {
            modal.showModal();
        }
    });
}

/**
 * Close a modal dialog
 * @param {string} modalId - The ID of the modal dialog element
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.close();
    }
}
