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
  formData.append("desc", $("#desc").val());

  $.ajax({
    url: "add-data",
    type: "post",
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response["result"] == "success") {
        localStorage.setItem('tambahData','true')
        window.location.replace("/data_mobil");
      } else {
        toastr.warning(response['msg']);
      }
    },
  });
}
