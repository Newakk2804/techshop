document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.newsletter form');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const emailInput = form.querySelector('input[type="email"]');
      const email = emailInput.value;

      fetch('/newsletters/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ email: email }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            showToast('✅ Спасибо за подписку!');
            emailInput.value = '';
          } else {
            showToast('⚠️ ' + (data.error || 'Ошибка подписки'));
          }
        });
    });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.style.marginBottom = '10px';
    toast.style.borderRadius = '5px';
    toast.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.transition = 'opacity 0.5s ease';
      toast.style.opacity = '0';
      setTimeout(() => {
        container.removeChild(toast);
      }, 500);
    }, 2000);
  }
});
