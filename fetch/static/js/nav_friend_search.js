document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('nav-friend-search');
  if (!form) return;

  const userInput = form.querySelector('[name="search_username"]');

  form.addEventListener('submit', async (e) => {
    e.preventDefault(); 
    const formData = new FormData(form);

    try {
      const resp = await fetch('/api/friend-request', {
        method: 'POST',
        body:   formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin'
      });
      const data = await resp.json();

      if (resp.ok && data.status === 'sent') {
        alert(`Friend request sent to ${data.username}!`);
      } else {
        alert(data.error || 'Something went wrong.');
      }
    } catch (_) {
      alert('Network error – please try again.');
    }

    form.reset();
    userInput.focus();
  });
});
