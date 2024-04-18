$(function () {
    var loader = 'https://thenounproject.com/icon/identity-897141/download/?i=897141&s=128';
    $('img[data-src]:not([src])').each(function () {
        var $img = $(this).attr('src', loader),
            src  = $img.data('src'),
            $clone = $img.clone().attr('src', src);
        $clone.on('load', function () {
            $img.attr('src', src);
        });d
    });
});


// function imgError(image) {
//     image.onerror = "";
//     image.src = "https://thenounproject.com/icon/identity-897141/download/?i=897141&s=128";
//     return true;
// }

// <img src="image.png" onerror="imgError(this);"/>