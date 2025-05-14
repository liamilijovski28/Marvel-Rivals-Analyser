document.addEventListener("DOMContentLoaded", function () {
    const sharingSelect = document.getElementById('data-sharing');
    const restrictedDiv = document.getElementById('restricted-friends-container');

    function toggleRestricted() {
        restrictedDiv.style.display =
            sharingSelect.value === 'yes' ? 'block' : 'none';
    }

    if (sharingSelect && restrictedDiv) {
        sharingSelect.addEventListener('change', toggleRestricted);
        toggleRestricted(); // Run on page load
    }
});

function showDisabledAlert(event) {
    event.preventDefault(); // prevent the form from submitting
    alert("Saving your account is currently disabled.");
}

function showCloseAlert() {
    alert("Closing your account is currently disabled. This feature is not available yet.");
}
