function createTransaction(id_mobil, user_id) {
  $('#btn_pesan').attr('disabled', true);
  var hari = $("#hari").val();
  $.ajax({
    url: "/api/create_transaction",
    type: "post",
    data: {
      hari: hari,
      id_mobil: id_mobil,
      user_id: user_id,
    },
    success: function (response) {
      if (response.status == "unpaid_transaction") {
        toastr.warning(response['message'], 'Notification', {
          onHidden: function() {
            $('#btn_pesan').attr('disabled', false);
          }
        });
      } else {
        window.location.replace(`/transaksi/${response.id}`);
      }
    },
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const hariInput = document.getElementById('hari');
  const totalPriceElement = document.getElementById('total_price');
  const hargaPerHari = parseInt(document.getElementById('harga_per_hari').value, 10);

  hariInput.addEventListener('input', function() {
    const hari = parseInt(hariInput.value);
    if (!isNaN(hari) && hari > 0) {
      const totalPrice = hargaPerHari * hari;
      totalPriceElement.textContent = 'Total Harga: Rp ' + totalPrice.toLocaleString('id-ID');
    } else {
      totalPriceElement.textContent = 'Total Harga: Rp 0';
    }
  });
});
