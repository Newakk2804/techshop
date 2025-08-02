document.addEventListener('DOMContentLoaded', () => {
  window.ProductInteractions.updateCartCount();

  document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
    button.addEventListener('click', e => {
      e.preventDefault();

      const cartItemId = button.getAttribute('data-cart-item-id');
      const row = button.closest('.cart-item-row');

      fetch('/cart/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.ProductInteractions.getCookie('csrftoken'),
        },
        body: JSON.stringify({ cart_item_id: cartItemId }),
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          row.remove();
          document.getElementById('cart-total-price').innerText = data.total_price + ' BYN';
          document.getElementById('cart-total-quantity').innerText = data.total_quantity;
          window.ProductInteractions.updateCartCount();
          window.ProductInteractions.showToast('❌ Товар удалён из корзины.', 'success');

          if (!document.querySelectorAll('.cart-item-row').length) {
            document.querySelector('.content-cart').innerHTML = `
              <div class="text-center" style="padding: 8px 0;">
                <h4 class="text-muted">Ваша корзина пуста.</h4>
              </div>`;
          }
        }
      });
    });
  });
});
