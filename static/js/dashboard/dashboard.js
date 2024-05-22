

function logout() {
  $.removeCookie("token", { path: "/" });
  window.location.reload();
}

function hideSidebar() {
  $(".logo h4").toggleClass("d-none");
  $(this).toggle(function () {
    $("body").css("grid-template-columns", "5rem 1fr 1fr");
  });
}
