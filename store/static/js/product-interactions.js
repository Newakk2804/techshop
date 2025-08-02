window.ProductInteractions = {
  cartHandler: null,
  wishlistHandler: null,

  init() {
    this.cartHandler = this._handleCartClick.bind(this);
    this.wishlistHandler = this._handleWishlistClick.bind(this);

    this.initCartButtons();
    this.initWishlistButtons();
    this.updateCartCount();
    this.updateFavoriteCount();
  },

  initCartButtons() {
    document.removeEventListener('click', this.cartHandler);
    document.addEventListener('click', this.cartHandler);
  },

  _handleCartClick(e) {
    const btn = e.target.closest('.add-to-cart-btn');
    if (!btn) return;

    e.preventDefault();
    const productId = btn.dataset.productId;
    if (!productId) return;

    fetch('/cart/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCookie('csrftoken'),
      },
      body: JSON.stringify({ product_id: productId, quantity: 1 }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          this.showToast('✅ Товар добавлен в корзину!', 'success');
          this.updateCartCount();
        } else {
          this.showToast('⚠️ Ошибка при добавлении.', 'danger');
        }
      });
  },

  initWishlistButtons() {
    document.removeEventListener('click', this.wishlistHandler);
    document.addEventListener('click', this.wishlistHandler);
  },

  _handleWishlistClick(e) {
    const btn = e.target.closest('.add-to-wishlist');
    if (!btn) return;

    e.preventDefault();
    const productId = btn.dataset.productId;
    if (!productId) return;

    fetch('/favorite/toggle/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCookie('csrftoken'),
      },
      body: JSON.stringify({ product_id: productId }),
    })
      .then((res) => res.json())
      .then((data) => {
        const icon = btn.querySelector('i');
        if (data.status === 'added') {
          icon?.classList.remove('fa-heart-o');
          icon?.classList.add('fa-heart');
          this.showToast('✅ Товар добавлен в избранные!', 'success');
        } else if (data.status === 'removed') {
          icon?.classList.remove('fa-heart');
          icon?.classList.add('fa-heart-o');
          this.showToast('❌ Товар удалён из избранных.', 'success');
        }

        this.updateFavoriteCount();

        // Если мы на странице избранного — удалим карточку
        if (window.location.pathname === '/favorite/') {
          const card = document.getElementById(`favorite-product-${productId}`);
          if (card) {
            card.remove();

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
  },

  updateCartCount() {
    fetch('/cart/count/')
      .then((res) => res.json())
      .then((data) => {
        const el = document.getElementById('cart-qty');
        if (el) el.textContent = data.count;
      });
  },

  updateFavoriteCount() {
    fetch('/favorite/count/')
      .then((res) => res.json())
      .then((data) => {
        const el = document.getElementById('favorite-count');
        if (el) el.textContent = data.count;
      });
  },

  showToast(message, type = 'info') {
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
      setTimeout(() => container.removeChild(toast), 500);
    }, 2000);
  },

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      for (let cookie of document.cookie.split(';')) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  },
};

document.addEventListener('DOMContentLoaded', () => {
  window.ProductInteractions.init();
});
