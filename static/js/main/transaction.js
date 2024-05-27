function cancelPayment(order_id){
    $.ajax({
        url: "/api/cancelPayment",
        type: "POST",
        data : {
            order_id: order_id
        },
        success: function (response) {
            alert('anda membatalkan transaksi')
            window.location.reload()
        }
    })
}

function addStatusLabel(){
    $("tr#unpaid").each(function () {
      $(this).addClass("table-warning");
    });
  }

  $(document).ready(function () {
    addStatusLabel();
  })