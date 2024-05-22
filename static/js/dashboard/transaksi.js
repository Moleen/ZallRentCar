$(document).ready(function () {
    addStatusLabel()
})

function addStatusLabel(){
    $("tr td#status").each(function () {
      var status = $(this).text();
      if (status == "sudah bayar") {
        $(this).parent().addClass("table-success");
      } else if(status ==="Diproses"){
        $(this).parent().addClass("table-warning");
      }else{
        $(this).parent().addClass("table-danger");
      }
    });
  }