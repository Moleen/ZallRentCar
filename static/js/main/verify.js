function sendVerify(user_id) {
  $(this).attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/api/verify",
    data: {
      user_id: user_id,
    },
    success: function (data) {
        window.location.reload()
    },
  });
}

function verifyKode(user_id){
    kode = $('#kodeVerif').val()
    $.ajax({
        type: "POST",
        url: "/api/verify_kode",
        data: {
            user_id: user_id,
            kode: kode
            },
            success: function (data) {
                if(data['result'] == 'success'){
                    window.location.href = '/'
                }else{
                    alert('Kode verifikasi salah')
                }
            }
    })
}
function logout() {
  Swal.fire({
    position: "top",
    text: "Anda yakin untuk logout?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes",
  }).then((result) => {
    if (result.isConfirmed) {
      $.removeCookie("tokenMain");
      localStorage.setItem("logout", "true");
      window.location.replace("/");
    }
  });
}
