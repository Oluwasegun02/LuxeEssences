
// $(document).ready(function () {
//   $('.paywithPayStack').click(function (e) {
//     e.preventDefault();

//     // Retrieve form values
//     var fname = $("[name='fname']").val();
//     var lname = $("[name='lname']").val();
//     var city = $("[name='city']").val();
//     var country = $("[name='country']").val();
//     var email = $("[name='email']").val();
//     var phone = $("[name='phone']").val();
//     var address = $("[name='address']").val();
//     var pincode = $("[name='pincode']").val();
//     var state = $("[name='state']").val();

//     // Check if any required fields are empty
//     if (fname === "" || lname === "" || city === "" || email === "" || country === "" || phone === "" || address === "" || state === "" || pincode === "") {
//       swal("Alert!", "All fields are mandatory", "error");
//       return false;
//     } else {
//       // Perform server-side verification if needed (optional)

//       // Initialize Paystack
//       var totalAmount = parseFloat(document.getElementById('amount').innerText.replace('$', '').trim()) * 100; // Convert to kobo (lowest currency unit)
//       var handler = PaystackPop.setup({
//         key: 'pk_test_9ff6885640ee828c677033aec652b991ced7f846', // Replace with your public key
//         email: email,
//         amount: totalAmount * 900, // Convert to kobo (lowest currency unit)
//         currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars
//         ref: 'khfdghfsdghsdgkshfgs', // Replace with a reference you generated
//         callback: function (response) {
//           // This function is called after a successful payment
//           var reference = response.reference;
//           alert('Payment complete! Reference: ' + reference);

//           // Make an AJAX call to your server to verify the transaction
//           $.ajax({
//             method: "POST", // Change to POST for security
//             url: "/verify", // Specify the URL for verifying the transaction on your server
//             data: {
//               name: fname+" "+lname,
//               email: email,
//               contact: phone,
//               reference: reference
//             },
//             success: function (verificationResponse) {
//               // Handle the verification response from your server
//               console.log(verificationResponse);
//             },
//             error: function (xhr, textStatus, errorThrown) {
//               // Handle AJAX request errors here
//               console.error('AJAX error:', textStatus, errorThrown);
//             }
//           });
//         },
//         onClose: function () {
//           alert('Transaction was not completed, window closed.');
//         },
//       });

//       // Open the Paystack payment iframe
//       handler.openIframe();
//     }
//   });
// });



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

    if (fname == "" || lname == "" || city == "" || email == "" || country == "" || phone == "" || address == "" || state == "" || pincode == "") {
      swal("Alert!", "All fields are mandatory", "error");
      return false;
    } else {
      // Make an AJAX request to retrieve order details
      $.ajax({
        method: "GET",
        url: "/verify",
        success: function (response) {
          var options = {
            key: 'pk_test_9ff6885640ee828c677033aec652b991ced7f846', // Replace with your public key
            email: email,
            amount: response.total_price * 100 * 900, // Convert to kobo (lowest currency unit)
            currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars
            ref: response.tracking_no, // Use the tracking_no from the response
            callback: function (responsea) {
              alert(responsea.reference); // Use responsea.reference for the payment reference

              // Prepare data for the /placeorder endpoint
              var data = {
                "fname": fname,
                "lname": lname,
                "city": city,
                "country": country,
                "email": email,
                "phone": phone,
                "address": address,
                "pincode": pincode,
                "state": state,
                "payment_mode": "paid by paystack",
                "payment_id": responsea.reference, // Use responsea.reference as payment_id
                csrfmiddlewaretoken: token
              };

              // Make an AJAX request to /placeorder to complete the order
              $.ajax({
                method: "POST",
                url: "/placeorder",
                data: data,
                success: function (responseb) {
                  swal("Congratulations!", responseb.status, "success").then(function () {
                    window.location.href = '/my-orders';
                  });
                },
                error: function (xhr, textStatus, errorThrown) {
                  console.error('AJAX error:', textStatus, errorThrown);
                }
              });
            },
            onClose: function () {
              alert('Transaction was not completed, window closed.');
            },
          };

          // Initialize Paystack
          var handler = PaystackPop.setup(options);

          // Open the Paystack payment iframe
          handler.openIframe();
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log('AJAX error:', textStatus, errorThrown);
        }
      });
    }
  });
});
