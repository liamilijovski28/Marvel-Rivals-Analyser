document.addEventListener('DOMContentLoaded', () => {
    /* Toggle dropdown menu when "..." button clicked */
    document.querySelectorAll('.dropdown-toggle').forEach(button => {
      button.addEventListener('click', event => {
        event.stopPropagation();
        const dropdown = button.parentElement;
        dropdown.classList.toggle('show');
      });
    });
  
    /* Close any open dropdowns when clicking outside */
    document.addEventListener('click', event => {
      document.querySelectorAll('.dropdown').forEach(dropdown => {
        if (!dropdown.contains(event.target)) {
          dropdown.classList.remove('show');
        }
      });
    });
  
    /* Close the dropdown when clicking "Remove Friend" or "Cancel" */
    document.querySelectorAll('.remove-friend-dropdown').forEach(button => {
      button.addEventListener('click', event => {
        const dropdown = button.closest('.dropdown');
        dropdown.classList.remove('show');
      });
    });
  });
