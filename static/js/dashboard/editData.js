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