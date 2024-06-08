function createTransaction(id_mobil, user_id) {
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
      if (response.status == "success") {
        window.location.replace(`/transaksi/${response.id}`);
      } else if (response.status == "NotLoggedIn") {
        window.location.replace(`/login?msg=${response.msg}`);
      } else if(response.status == "unpaid_transaction"){
        alert(response.message)
      }
    },
  });
}
