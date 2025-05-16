document.addEventListener('DOMContentLoaded', () => {
  const hideAllDropdowns = () =>
    document.querySelectorAll('.confirm-box')
            .forEach(box => box.style.display = 'none');

  /* open / toggle confirmation */
  document.querySelectorAll('.remove-trigger').forEach(trigger => {
    trigger.addEventListener('click', e => {
      e.stopPropagation();
      const box = trigger.parentElement.querySelector('.confirm-box');
      if (!box) return;

      const isOpen = box.style.display === 'flex';
      hideAllDropdowns();
      if (!isOpen) box.style.display = 'flex';
    });
  });

  /* close when “Cancel” is clicked */
  document.addEventListener('click', e => {
    if (e.target.matches('.cancel-remove')) {
      e.target.closest('.confirm-box').style.display = 'none';
      return;
    }
    /* close when clicking anywhere outside an open box */
    if (!e.target.closest('.confirm-box') &&
        !e.target.closest('.remove-trigger')) {
      hideAllDropdowns();
    }
  });
});
