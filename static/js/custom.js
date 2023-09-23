$(document).ready(function () {

  $('.increment-btn').click(function (e){
    e.preventDefault();

    var inc_value = $(this).closest('.product_data').find('.qty-input').val();
    var value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;
    if(value < 10)
    {
      value++;
      $(this).closest('.product_data').find('.qty-input').val(value);
    }
  });
  $('.decrement-btn').click(function (e) {
    e.preventDefault();

    var dec_value = $(this).closest('.product_data').find('.qty-input').val();
    var value = parseInt(dec_value, 10);
    value = isNaN(value) ? 0 : value;
    if(value > 1)
    {
      value--;
      $(this).closest('.product_data').find('.qty-input').val(value);
    }
  });

  $('.addToCartBtn').click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
      method: "POST",
      url: "/add-to-cart",
      data: {  // Use curly braces to define an object
        'product_id': product_id,
        'product_qty': product_qty,
        csrfmiddlewaretoken: token, // Note the comma here
      },
      success: function (response) {
        alertify.success(response.status);
        
      }
    });
  });

  $('.addToWishlist').click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var token = $('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
      method: "POST",
      url: "/add-to-wishlist",
      data: {  // Use curly braces to define an object
        'product_id': product_id,
        csrfmiddlewaretoken: token, // Note the comma here
      },
      success: function (response) {
        alertify.success(response.status);
        
      }
    });
  });
  
  $('.changeQuantity').click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
      method: "POST",
      url: "/update-cart",
      data: {  // Use curly braces to define an object
        'product_id': product_id,
        'product_qty': product_qty,
        csrfmiddlewaretoken: token, // Note the comma here
      },
      success: function (response) {
        // alertify.success(response.status);
        
      }
    });
  });

  $(document).on('click','.delete-cart-item', function (e) {
      e.preventDefault();
    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var token = $('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
      method: "POST",
      url: "/delete-cart-item",
      data: {
        'product_id': product_id,
        csrfmiddlewaretoken: token,  
      },
      success: function (response) {
        alertify.success(response.status);
        $('.cartdata').load(location.href + " .cartdata");
      }
    });
  });


  $(document).on('click','.delete-wishlist-item', function (e) {
      e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var token = $('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
      method: "POST",
      url: "/delete-wishlist-item",
      data: {
        'product_id': product_id,
        csrfmiddlewaretoken: token,  
      },
      success: function (response) {
        alertify.success(response.status);
        $('.wishdata').load(location.href + " .wishdata");
      }
    });
    
  });

});
