document.addEventListener('DOMContentLoaded', function () {
  updateCartCount();
  const cartButtons = document.querySelectorAll('.add-to-cart-btn');
  const removeButtons = document.querySelectorAll('.remove-from-cart-btn');

  cartButtons.forEach((button) => {
    button.addEventListener('click', function (e) {
      e.preventDefault();

      const productId = this.getAttribute('data-product-id');

      fetch('/cart/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            showToast('✅ Товар добавлен в корзину!', 'success');
            updateCartCount();
          } else {
            showToast('⚠️ Ошибка при добавлении.', 'danger');
          }
        });
    });
  });

  removeButtons.forEach((button) => {
    button.addEventListener('click', function (e) {
      e.preventDefault();

      const cartItemId = this.getAttribute('data-cart-item-id');
      const productCard = this.closest('.cart-item-row');

      fetch('/cart/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ cart_item_id: cartItemId }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            productCard.remove();
            document.getElementById('cart-total-price').innerText = data.total_price + ' BYN';
            document.getElementById('cart-total-quantity').innerText = data.total_quantity;
            showToast('❌ Товар удалён из корзины.', 'success');
            updateCartCount();

            // Проверяем, остались ли товары в корзине
            const cartItems = document.querySelectorAll('.cart-item-row');
            if (cartItems.length === 0) {
              // Корзина пустая — показываем сообщение
              const container = document.querySelector('.content-cart'); // или другой подходящий селектор родителя корзины
              container.innerHTML = `
              <div class="text-center" style="padding: 8px 0;">
                <h4 class="text-muted">Ваша корзина пуста.</h4>
              </div>
            `;
            }
          } else {
            showToast('⚠️ Не удалось удалить товар.', 'danger');
          }
        });
    });
  });

  function updateCartCount() {
    fetch('/cart/count/')
      .then((res) => res.json())
      .then((data) => {
        const cartCounter = document.getElementById('cart-qty');
        if (cartCounter) {
          cartCounter.textContent = data.count;
        }
      });
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
});
