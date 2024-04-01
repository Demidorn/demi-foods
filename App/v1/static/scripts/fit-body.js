window.addEventListener('scroll', function () {
    var content = document.getElementById('header');
    var scrollTop = window.scrollY || document.documentElement.scrollTop;
    // Determine whether to fix body based on scroll position
    if (scrollTop > 100) { // For example, scroll threshold
        content.classList.add('fixed-body');
    } else {
        content.classList.remove('fixed-body');
    }
});