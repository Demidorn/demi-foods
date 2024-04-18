$('.like-btn').on('click', function() {
    $(this).toggleClass('is-active');
 });

 $('.minus-btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
 
    if (value > 1) {
        value = value - 1;
    } else { 
        value = 0;
    }
 
  $input.val(value);
 
});
 
$('.plus-btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
 
    if (value < 100) {
        value = value + 1;
    } else {
        value =100;
    }
 
    $input.val(value);
});

// Function to format prices with Naira symbol
function formatPrice(price) {
    return '₦' + price.toFixed(2); 
}

// Example usage:
$('.price').each(function() {
    var price = parseFloat($(this).text());
    $(this).text(formatPrice(price));
});