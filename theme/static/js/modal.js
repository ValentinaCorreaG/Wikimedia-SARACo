/**
 * Generic Modal Management for DaisyUI + HTMX
 * 
 * This module provides reusable modal functionality across the application.
 * It handles:
 * - Opening modals when HTMX swaps content
 * - Closing modals on custom events
 * - Form reset and validation handling
 * - Delete confirmation modals
 * 
 * Usage:
 * 1. Add data-modal-target="modal-id" to HTMX targets to auto-open modals
 * 2. Trigger 'modalClose' event with detail: { modalId: 'modal-id', resetForm: true, formId: 'form-id' }
 * 3. Trigger 'formInvalid' event with detail: { modalId: 'modal-id' } to keep modal open
 * 4. Use ModalManager.showDeleteConfirm() for delete confirmations
 */

const ModalManager = {
    /**
     * Initialize modal event listeners
     */
    init: function() {
        this.setupHtmxModalOpen();
        this.setupModalClose();
        this.setupFormValidation();
    },

    /**
     * Open modal when HTMX swaps content into a target with data-modal-target
     */
    setupHtmxModalOpen: function() {
        document.body.addEventListener('htmx:afterSwap', function(event) {
            const target = event.detail?.target;
            if (!target) return;

            const modalId = target.dataset.modalTarget;
            if (modalId) {
                ModalManager.open(modalId);
            }
        });
    },

    /**
     * Listen for modal close events
     */
    setupModalClose: function() {
        document.body.addEventListener('modalClose', function(event) {
            const { modalId, resetForm, formId, contentId, reload } = event.detail || {};
            
            if (modalId) {
                ModalManager.close(modalId, { resetForm, formId, contentId, reload });
            }
        });
    },

    /**
     * Keep modal open when form validation fails
     */
    setupFormValidation: function() {
        document.body.addEventListener('formInvalid', function(event) {
            const modalId = event.detail?.modalId;
            if (modalId) {
                ModalManager.open(modalId);
            }
        });
    },

    /**
     * Open a modal by ID
     * @param {string} modalId - The ID of the dialog element
     */
    open: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal && typeof modal.showModal === 'function') {
            modal.showModal();
        }
    },

    /**
     * Close a modal and optionally reset form/clear content
     * @param {string} modalId - The ID of the dialog element
     * @param {Object} options - Configuration options
     * @param {boolean} options.resetForm - Whether to reset the form
     * @param {string} options.formId - ID of form to reset (optional)
     * @param {string} options.contentId - ID of content container to clear
     * @param {boolean} options.reload - Whether to reload the page after closing
     */
    close: function(modalId, options = {}) {
        const modal = document.getElementById(modalId);
        if (modal && typeof modal.close === 'function') {
            modal.close();
        }

        // Reset form if specified
        if (options.resetForm && options.formId) {
            const form = document.getElementById(options.formId);
            if (form) form.reset();
        }

        // Clear content container if specified
        if (options.contentId) {
            const content = document.getElementById(options.contentId);
            if (content) content.innerHTML = '';
        }

        // Reload page if specified
        if (options.reload) {
            location.reload();
        }
    },

    /**
     * Show a delete confirmation modal
     * @param {HTMLElement} trigger - The button that triggered the delete
     * @param {Object} config - Configuration for the delete modal
     * @param {string} config.modalId - ID of the delete modal
     * @param {string} config.displayId - ID of element to show the item name
     * @param {string} config.confirmBtnId - ID of the confirm button
     */
    showDeleteConfirm: function(trigger, config = {}) {
        const {
            modalId,
            displayId,
            confirmBtnId
        } = config;

        const itemName = trigger.dataset.name || trigger.dataset.username;
        const deleteUrl = trigger.dataset.deleteUrl;

        // Update modal content
        if (displayId) {
            const displayEl = document.getElementById(displayId);
            if (displayEl) {
                displayEl.textContent = itemName;
            }
        }

        // Update HTMX delete URL
        if (confirmBtnId && deleteUrl) {
            const confirmBtn = document.getElementById(confirmBtnId);
            if (confirmBtn) {
                confirmBtn.setAttribute('hx-delete', deleteUrl);
                htmx.process(confirmBtn);
            }
        }

        // Open the modal
        if (modalId) {
            this.open(modalId);
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    ModalManager.init();
});

// Expose globally for use in templates
window.ModalManager = ModalManager;

/**
 * Helper function for delete modals (used in onclick handlers)
 * @param {HTMLElement} button - The button that triggered the delete
 */
window.showDeleteModal = function(button) {
    ModalManager.showDeleteConfirm(button, {
        modalId: 'delete_user_modal',
        displayId: 'delete-username',
        confirmBtnId: 'confirm-delete-btn'
    });
};
