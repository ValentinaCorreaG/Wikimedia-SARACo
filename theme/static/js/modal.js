// Modal management for calendar and events

document.addEventListener('DOMContentLoaded', function() {
    // Open DaisyUI modal when HTMX swaps content into it
    document.body.addEventListener('htmx:afterSwap', function(ev) {
        if (ev.detail?.target?.id === 'modal-box-content') {
            document.getElementById('modal-container').showModal();
        }
    });

    // Close modal and clear content when form is submitted or modal is dismissed
    document.body.addEventListener('eventClosed', function() {
        var dialog = document.getElementById('modal-container');
        var box = document.getElementById('modal-box-content');
        if (dialog) dialog.close();
        if (box) box.innerHTML = '';
    });
});
