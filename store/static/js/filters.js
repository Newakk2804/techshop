$(document).ready(function () {
  function fetchFilteredProducts(newPage = null) {
    const params = new URLSearchParams();

    // Все данные формы, включая q из поля поиска
    $('#filter-form')
      .serializeArray()
      .forEach(({ name, value }) => {
        if (value) {
          params.append(name, value);
        }
      });

    if (newPage !== null) {
      params.set('page', newPage);
    } else {
      params.delete('page');
    }

    const queryString = params.toString();

    $.ajax({
      url: '/products/ajax/',
      type: 'GET',
      data: queryString,
      success: function (response) {
        $('#product-list').html(response.products_html);
        $('#pagination').html(response.pagination_html);

        const newUrl = window.location.pathname + '?' + queryString;
        window.history.pushState(null, '', newUrl);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error('AJAX error:', textStatus, errorThrown);
        console.error('Response text:', jqXHR.responseText);
        alert('Ошибка при загрузке товаров. Проверьте консоль для деталей.');
      },
    });
  }

  $('#filter-form input').on('change input', function () {
    fetchFilteredProducts();
  });

  $('#reset-filters').on('click', function () {
    $('#filter-form input[type=checkbox]').prop('checked', false);
    $('#filter-form input[type=number]').val('');
    $('#filter-form input[type=text]').val('');
    fetchFilteredProducts();
  });

  $(document).on('click', '.store-pagination a', function (e) {
    e.preventDefault();
    const url = new URL($(this).attr('href'), window.location.origin);
    const page = url.searchParams.get("page");
    fetchFilteredProducts(page);
  });
});
