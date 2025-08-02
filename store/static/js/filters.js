document.addEventListener('DOMContentLoaded', () => {
  function fetchFilteredProducts(newPage = null) {
    const form = document.getElementById('filter-form');
    if (!form) return;

    const params = new URLSearchParams(new FormData(form));

    if (newPage !== null) {
      params.set('page', newPage);
    } else {
      params.delete('page');
    }

    fetch(`/products/ajax/?${params.toString()}`, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then((res) => res.json())
      .then((data) => {
        const productList = document.getElementById('product-list');
        const pagination = document.getElementById('pagination');

        if (productList && data.products_html) {
          productList.innerHTML = data.products_html;
        }

        if (pagination && data.pagination_html) {
          pagination.innerHTML = data.pagination_html;
        }

        // Важно: повторная инициализация кнопок
        window.ProductInteractions.initCartButtons();
        window.ProductInteractions.initWishlistButtons();

        // Обновляем URL
        const newUrl = window.location.pathname + '?' + params.toString();
        window.history.pushState(null, '', newUrl);
      })
      .catch((err) => {
        console.error('Ошибка при фильтрации:', err);
        alert('Ошибка загрузки товаров.');
      });
  }

  const filterForm = document.getElementById('filter-form');
  if (filterForm) {
    filterForm.addEventListener('input', () => fetchFilteredProducts());
  }

  const resetBtn = document.getElementById('reset-filters');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      filterForm.reset();
      fetchFilteredProducts();
    });
  }

  // пагинация
  document.addEventListener('click', (e) => {
    const target = e.target.closest('.store-pagination a');
    if (!target) return;

    e.preventDefault();
    const url = new URL(target.href);
    const page = url.searchParams.get('page');
    fetchFilteredProducts(page);
  });
});
