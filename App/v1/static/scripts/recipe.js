const $ = window.$;
$(document).ready(function () {
  $('#sortable').sortable();
  $('#sortable').disableSelection();
});

$(document).ready(function () {
  // Event handler for form submission
  $('.btn-primary').click(function (event) {
    event.preventDefault(); // Prevent default form submission

    const form = $(this).closest('form'); // Find the closest form
    const quantityField = form.find("input[name='quantity']"); // Get quantity value
    const qtymsg = form.find('.text-danger'); // Find the validation message element
    const quantity = parseInt(quantityField.val());
    // Validate quantity
    if (quantity < 1 || isNaN(quantity)) {
      qtymsg.text('How many do you want?');
      return false; // Prevent form submission
    }
    // Submit the form if validation passes using ajax
    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: form.serialize(),
      dataType: 'json',
      success: function (response) {
        if (response.success) {
          qtymsg.removeClass('error').text('');
          quantityField.val('');
          $('#cartModal').modal('show');
          $('#cartModalLabel').html(response.message);
          updateCart(response.cart_items, response.all_total);
        } else {
          console.error('Failed to add item to cart');
        }
      },
      error: function (xhr, status, error) {
        console.error('Ajax error:', error);
      }
    });
  });
  // function creates and update the cart dynamically
  function updateCart (cartItems, allAmt) {
    const modalBody = $('#cartModal tbody');

    // modalBody.empty();

    let allTotal = allAmt;
    if (Array.isArray(cartItems)) {
      cartItems.forEach(function (cartItem) {
        const totalAmt = cartItem.price * cartItem.quantity;
        const modalHtml = `
       
         <tr>
            <td class="w-25">
              <img src="${cartItem.image_path}" class="img-fluid img-thumbnail" alt="${cartItem.food_name}">
            </td>
            <td>${cartItem.food_name}</td>
            <td>₦${cartItem.price}</td>
            <td class="qty">${cartItem.quantity}</td>
            <td>₦${totalAmt}</td>
            <td>
              <button class="btn btn-danger btn-sm remove-item" data-product-id="">
                <i class="fa fa-times"></i>
              </button>
            </td>
          </tr>

        `;
        modalBody.append(modalHtml);
        allTotal += totalAmt;
      });
    } else {
      console.error('cartItems is not Array');
    }
    $('.text-success').text('₦' + allTotal.toFixed(2));
  }

  $('#cartModal .close, .btn-secondary').click(function(event) {
    $('#cartModal').modal('hide');
  });
});
