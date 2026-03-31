/**
 * SARA Permission Error Handler
 * 
 * Handles 403 Forbidden responses from HTMX requests and displays
 * a toast notification to the user.
 */

document.body.addEventListener('htmx:responseError', function(event) {
    // Check if it's a 403 Forbidden error
    if (event.detail.xhr.status === 403) {
        // Show error toast
        showErrorToast('No tienes permisos para realizar esta acción.');
        
        // Prevent HTMX from processing the response further
        event.detail.shouldSwap = false;
        event.detail.isError = false;
    }
});

/**
 * Show an error toast notification
 * @param {string} message - The error message to display
 */
function showErrorToast(message) {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast toast-top toast-end pointer-events-none';
        document.body.appendChild(toastContainer);
    }

    // Create toast element with DaisyUI alert styling
    const toast = document.createElement('div');
    toast.className = 'alert alert-error pointer-events-auto';
    toast.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l-2-2m0 0l-2-2m2 2l2-2m-2 2l-2 2m2-2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Show a success toast notification
 * @param {string} message - The success message to display
 */
function showSuccessToast(message) {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast toast-top toast-end pointer-events-none';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = 'alert alert-success pointer-events-auto';
    toast.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Show an info toast notification
 * @param {string} message - The info message to display
 */
function showInfoToast(message) {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast toast-top toast-end pointer-events-none';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = 'alert alert-info pointer-events-auto';
    toast.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}
