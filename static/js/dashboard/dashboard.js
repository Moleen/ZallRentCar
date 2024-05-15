$(document).ready(function () {
    var current = location.pathname;
    $(".nav .nav-item .nav-link").each(function () {
      var $this = $(this);
      // if the current path is like this link, make it active
      if ($this.attr("href") == current) {
        $this.addClass("active");
      }
    });
});

function logout() {
  $.removeCookie("token", { path: "/" });
  window.location.reload();
}

function hideSidebar(){
  $('.logo h4').toggleClass('d-none')
  $(this).toggle(function (){
    $('body').css( "grid-template-columns", "5rem 1fr 1fr" )
  });
}
