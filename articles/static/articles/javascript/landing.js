window.addEventListener('load', function () {
    const loader = document.querySelector('.loader');
    loader.classList.add('done');
    AOS.init();

});
mybutton = document.getElementById('myBtn');

window.onscroll = function () {
    scrollFunction();
};
function scrollFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        mybutton.style.display = 'block';
    } else {
        mybutton.style.display = 'none';
    }
}
// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
$(document).ready(function () {
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
    });
});
