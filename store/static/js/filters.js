$(document).ready(function () {
  function fetchFilteredProducts() {
    const data = $('#filter-form').serialize();

    $.ajax({
      url: '/products/ajax/',
      type: "GET",
      data: data,
      success: function (response) {
        $('#product-list').html(response);
      },
      error: function () {
        alert("Ошибка при фильтрации товаров.");
      }
    });
  }

  // Обработка изменения фильтров
  $('#filter-form input').on('change input', function () {
    fetchFilteredProducts();
  });

  // Обработка сброса фильтров
  $('#reset-filters').on('click', function () {
    // Сбросить все чекбоксы
    $('#filter-form input[type=checkbox]').prop('checked', false);
    // Очистить все input[type=number] (например, цены)
    $('#filter-form input[type=number]').val('');
    // Запустить обновление товаров без фильтров
    fetchFilteredProducts();
  });
});