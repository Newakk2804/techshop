document.addEventListener('DOMContentLoaded', function () {
  updateFavoriteCount();
  const buttons = document.querySelectorAll('.add-to-wishlist');

  buttons.forEach((btn) => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.dataset.productId;

      fetch('/favorite/toggle/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === 'added') {
            this.querySelector('i').classList.remove('fa-heart-o');
            this.querySelector('i').classList.add('fa-heart');
          } else if (data.status === 'removed') {
            this.querySelector('i').classList.remove('fa-heart');
            this.querySelector('i').classList.add('fa-heart-o');
          }

          updateFavoriteCount();

          if (window.location.pathname === '/favorite/') {
            const card = document.getElementById(`favorite-product-${productId}`);
            if (card) {
              card.remove();

              // Если карточек не осталось, показываем сообщение
              const remaining = document.querySelectorAll('.product');
              if (remaining.length === 0) {
                const container = document.querySelector('.content-cards');
                container.innerHTML = `
                  <div class="text-center" style="padding: 76px 0">
                    <h4 class="text-muted">У вас пока нет избранных товаров.</h4>
                  </div>
                `;
              }
            }
          }
        });
    });
  });

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

  function updateFavoriteCount() {
    fetch('/favorite/count/')
      .then((res) => res.json())
      .then((data) => {
        const counter = document.getElementById('favorite-count');
        if (counter) {
          counter.textContent = data.count;
        }
      });
  }
});
