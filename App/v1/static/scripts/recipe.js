const $ = window.$;
$(document).ready(function () {
  $('#sortable').sortable();
  $('#sortable').disableSelection();

  // When "Add to Cart" button is clicked, show the modal
  //  $('.btn-primary').click(function (event) {
  //    event.preventDefault();
  //    $('#qtyform').submit();
  //    $('#cartModal').modal('show');
  //  });

  // script to validate form before showing the modal

  //  $('#qtyform').submit(function (event) {
  // console.log('form submitted');
  //    const qtyVal = parseInt($('#quantity').val());
  //  if (qtyVal < 1 || isNaN(qtyVal)) {
  //  event.preventDefault();
  //      $('#qtymsg').text('How many do you need?').show();
  //      $('#quantity').addClass('error');
  //      $('#quantity').focus();
  //    } else {
  //      $('#qtymsg').removeClass('error');
  //      $('#cartModal').modal('show');
  //    }
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
        } else {
          console.error('Failed to add item to cart');
        }
      },
      error: function (xhr, status, error) {
        console.error('Ajax error:', error);
      }
    });
  });
});
