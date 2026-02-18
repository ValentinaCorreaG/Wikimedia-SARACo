// Calendar interactions and modal management

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        const messagesEl = document.getElementById('messages');
        if (messagesEl) {
            messagesEl.style.opacity = '0';
            messagesEl.style.transition = 'opacity 0.5s';
            setTimeout(() => messagesEl.remove(), 500);
        }
    }, 5000);

    // Open DaisyUI modal when HTMX swaps content into it
    document.body.addEventListener('htmx:afterSwap', function(ev) {
        if (ev.detail?.target?.id === 'modal-box-content') {
            document.getElementById('modal-container').showModal();
        }
    });

    // Close modal and clear content when form is submitted or modal is dismissed
    document.body.addEventListener('eventClosed', function() {
        let dialog = document.getElementById('modal-container');
        let box = document.getElementById('modal-box-content');
        if (dialog) dialog.close();
        if (box) box.innerHTML = '';
    });
});
