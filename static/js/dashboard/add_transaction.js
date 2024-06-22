import { addStatusLabel, changeCurrency } from "./function.js";

$(document).ready(function () {
  addStatusLabel();
  changeCurrency();
  $(".owl-carousel").owlCarousel();
});

// $(document).on("click", function () {
//   $(".item-car").removeClass("selected");
//   $("#val_merek").html('');
//   $("#val_harga").html('');
// });

$(".item-car").each(function (index) {
  $(this).on("click", function (event) {
    event.stopPropagation();
    $('#hari').val('')
    $('#val_total').html('')
    $(".item-car").removeClass("selected");
    $(this).addClass("selected");
    let id_mobil = $(this).attr("id")

    $.ajax({
      type: "GET",
      url: "/api/get_car/" + id_mobil,
      success: function (response) {
        $("#val_merek").html(response["merek"]);
        $("#val_merek").attr('data-id', id_mobil)
        $("#val_harga").html(response["harga"]);
        $('#hari').on('keyup', function(){
          var value = $(this).val();
          $('#val_total').html(value * response["harga"])
          changeCurrency();
        })
        changeCurrency();
      },
    });
  });
});

$('#btn_bayar').on('click', function(){
  var id_mobil = $('#val_merek').attr('data-id')
  var hari = $('#hari').val()
  var total = $('#val_total').text()
  var bayar = $('#pembayaran').val()

  if(bayar == 'cash'){
    Swal.fire({
      position: "top",
      text: `konfirmasi pembayaran cash dengan total Rp. ${total}`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          url: '/api/add_transaction_from_admin',
          data: {
            mtd : 'cash',
            id_mobil: id_mobil,
            hari : hari
          },
          success: function (response) {
            if(response['result'] == 'success'){
              toastr.success(response['message'], 'Notification', {
                onHidden: function() {
                    window.location.replace('/transaction')
                }
            });
            }else{
              toastr.warning('Transaksi Gagal')
            }
          },
        });
      }
    });
  }
})



$(".owl-carousel").owlCarousel({
  loop: false,
  margin: 10,
  nav: false,
  responsive: {
    0: {
      items: 1,
    },
    600: {
      items: 2,
    },
    1000: {
      items: 4,
    },
  },
});
