$(".footer").remove();

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};

$("#btn_email_forgot_password").on("click", function () {
  var email = $("#email_forgot_password").val();
  $(this).attr('disabled',true)
  $.ajax({
    type: "POST",
    url: "/forgot_pass",
    data: { 
        email: email,
        from : 'users'
    },
    success: function (response) {
      if (response['result'] == 'success') {
        toastr.success(response['message'], 'Notification', {
            onHidden: function() {
                window.location.replace('/login')
            }
        })
      } else {
        toastr.error(response['message'])
        $('#btn_email_forgot_password').attr('disabled',false)
      }
    },
  });
});
