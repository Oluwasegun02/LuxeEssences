
$(document).ready(function () {
  // Get the quantity input element
  var quantityInput = $('#quantity-input');

  // Handle the click event for the increment button
  $('.increment-btn').click(function (e) {
    e.preventDefault();

    // Get the current value of the input field
    var value = parseInt(quantityInput.val(), 10);

    // Check if the value is a number; if not, default to 1
    if (isNaN(value)) {
      value = 1;
    }

    // Increment the value and update the input field
    value++;
    quantityInput.val(value);
  });

  // Handle the click event for the decrement button
  $('.decrement-btn').click(function (e) {
    e.preventDefault();

    // Get the current value of the input field
    var value = parseInt(quantityInput.val(), 10);

    // Check if the value is a number and greater than 1
    if (!isNaN(value) && value > 1) {
      // Decrement the value and update the input field
      value--;
      quantityInput.val(value);
    }
  });
  $('.addToCartBtn').click(function (e) {
    e.preventDefault();
    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $('#product-id').text('Product ID: ' + product_id);
    $('#product-qty').text('Quantity: ' + product_qty);
  
    $.ajax({
      method: "POST",
      url: "/add-to-cart",
      data: {  // Use curly braces to define an object
        'product_id': product_id,
        'product_qty': product_qty,
        'csrfmiddlewaretoken': token  // Note the comma here
      },
      success: function (response) {
        console.log(response);
        alertify.success(response.status);
        
      }
    });
  });
});



$(document).ready(function () {
  
  $('.paywithPayStack').click(function (e) {
    e.preventDefault();

    var fname = $("[name='fname']").val();
    var lname = $("[name='lname']").val();
    var city = $("[name='city']").val();
    var country = $("[name='country']").val();
    var email = $("[name='email']").val();
    var phone = $("[name='phone']").val();
    var address = $("[name='address']").val();
    var pincode = $("[name='pincode']").val();
    var state = $("[name='state']").val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    if(fname == "" || lname == "" || city == "" || email == "" || country == "" || phone == "" || address == "" || state == "" || pincode == ""){
      swal("Alert!", "All fields are mandatory", "error");
      return false;
    }
    else{
      $.ajax({
        method: "GET",
        url: "/verify",
        success: function (response) {
          var options = {
            key: 'pk_test_9ff6885640ee828c677033aec652b991ced7f846', // Replace with your public key
            email: email,
            amount: response.total_price, // the amount value is multiplied by 100 to convert to the lowest currency unit
            currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars
            ref: responce.tracking_no, // Replace with a reference you generated
            "handler": fuction (responsea){
              alert(responsea.paystack_payment_id);
              data = {
                "fname" : fname,
                "lname" :lname,
                "city ":   city,
                "country" :country,
                "email" :email,
                "phone" :phone,
                "address" :address,
                "pincode" :pincode,
                "state" :state,
                "payment_mode": "paid by paystack",
                "payment_id": responsea.paystack_payment_id,
                csrfmiddlewaretoken: token
              }
              $ajax({
                method: "POST",
                url: "/placeorder",
                data: data,
                success: fuction (responseb){
                  swal("Congratullations!", responseb.status, "success").then(value) => (
                    window.location.herf = '/my-orders'
                  )
                  swal(responseb.status)
                }
              })
            
            }
            },
            onClose: function() {
              alert('Transaction was not completed, window closed.');
            },
          });
          var repl = new Paystack(options);
          repl.open()
          // handler.openIframe();
        }
      })
   
    }
    
  })
  
});