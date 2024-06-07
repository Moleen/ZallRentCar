$(document).ready(function () {
  $("#input-file").change(function (e) {
    file = this.files[0];
    if (file) {
      let reader = new FileReader();
      reader.onload = function (event) {
        $("#imgPreview").attr("src", event.target.result);
        $("#imgPreview").removeAttr("hidden");
      };
      reader.readAsDataURL(file);
    }
  });
});

function addData() {
  var formData = new FormData();
  formData.append("gambar", $("#input-file")[0].files[0]);
  formData.append("merek", $("#merek").val());
  formData.append("seat", $("#seat").val());
  formData.append("transmisi", $("#transmisi").val());
  formData.append("harga", $("#harga").val());

  $.ajax({
    url: "add-data",
    type: "post",
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response["result"] == "success") {
        alert(`berhasil : ${response["result"]}`);
        window.location.replace("/dashboard/data_mobil");
      } else {
        alert(response["msg"]);
      }
    },
  });
}
