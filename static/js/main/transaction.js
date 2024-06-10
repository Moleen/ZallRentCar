function cancelPayment(order_id) {
  Swal.fire({
    position: "top",
    text: "Anda yakin ingin membatalkan transaksi?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes",
  }).then((result) => {
    if (result.isConfirmed) {
      // jika terkonfirmasi jalankan ajax
      $.ajax({
        url: "/api/cancelPayment",
        type: "POST",
        data: {
          order_id: order_id,
        },
        success: function (response) {
          // alert("anda membatalkan transaksi");
          localStorage.setItem('dataDeleted','true')
          location.reload();
        },
      });
    } 
  });
}

function addStatusLabel() {
  $("tr#unpaid").each(function () {
    $(this).addClass("table-warning");
  });
}

function alertAfter(){
  if(localStorage.getItem('dataDeleted') == 'true'){
    toastr.success('Pesananan sudah dibatalkan');
    localStorage.removeItem('dataDeleted')
  }
}

$(document).ready(function () {
  addStatusLabel();
  alertAfter();
});
