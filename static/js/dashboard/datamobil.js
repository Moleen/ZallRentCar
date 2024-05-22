$(document).ready(function () {
  
    $("#search-data").keyup(function () {
      var search = $(this).val();
      $.ajax({
        url: "/api/search-dashboard",
        type: "GET",
        data: { search: search },
        success: function (data) {
          $("#list-data").empty();
          var temp = "";
          if (data.length === 0) {
            var temp =
              "<tr><td colspan='7' class='text-center'>No Data</td></tr>";
            $("#list-data").append(temp);
          } else {
            for (let i = 0; i < data.length; i++) {
              var temp = `<tr>
                   <th scope="row">${i + 1}</th>
                   <td>${data[i].merek}</td>
                   <td>${data[i].model}</td>
                   <td>${data[i].tahun}</td>
                   <td>${data[i].warna}</td>
                   <td>${data[i].harga}</td>
                   <td id="status">${data[i].status}</td>
                 </tr>`;
              $("#list-data").append(temp);
            }
          }
          addStatusLabel()
        },
      });
    });
  
    addStatusLabel()
    
  });
  
  function addStatusLabel(){
    $("tr td#status").each(function () {
      var status = $(this).text();
      if (status === "Tersedia") {
        $(this).parent().addClass("table-success");
      } else if(status ==="Diproses"){
        $(this).parent().addClass("table-warning");
      }else{
        $(this).parent().addClass("table-danger");
      }
    });
  }

  // function changeStatus(status,ordeid){
  //   if (status == 'Diproses'){
  //     alert('Pastikan User telah mengambil mobil')
  //     $.ajax({
  //       url: "/api/change-status",
  //       type: "POST",
  //       data: { ordeid: ordeid, status: status },
  //       success: function (data) {
  //         window.location.reload()
  //         },
  //     })
  //   }
  // }