$(document).ready(function () {
  addStatusLabel();
  changeCurrency();

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
            if (data[i].status == "Diproses") {
              button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" onclick="confirmPesanan('{{dt.status}}','{{dt.order_id}}')"
                         role="button">Konfirmasi Pesanan</a></li>
                         </ul>`;
            } else if (data[i].status == "Digunakan") {
              button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" onclick="confirmPesanan('{{dt.status}}','{{dt.order_id}}')"
                         role="button">Konfirmasi Kembali</a></li>
                         </ul>`;
            } else {
              button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" href="/data_mobil/edit?id=${data[i].id_mobil}">Edit Mobil</a></li>
                         </ul>`;
            }
            var temp = `<tr>
                   <td>${i + 1}</td>
                   <td id="merek">${data[i].merek}</td>
                   <td>${data[i].seat}</td>
                   <td>${data[i].transmisi}</td>
                   <td data-target="currency">${data[i].harga}</td>
                   <td id="status">${data[i].status}</td>
                   <td>
                   <button class="btn fa-solid fa-edit" type="button" data-bs-toggle="dropdown"
                     aria-expanded="false"></button>
                    ${button}
                 </td>
                 </tr>`;
            $("#list-data").append(temp);
          }
        }
        addStatusLabel();
        changeCurrency();
      },
    });
  });
});

function addStatusLabel() {
  $("tr td#status").each(function () {
    var status = $(this).text();
    if (status === "Tersedia") {
      $(this).parent().addClass("table-success");
    } else if (status === "Diproses") {
      $(this).parent().addClass("table-warning");
    } else {
      $(this).parent().addClass("table-danger");
    }
  });
}

function changeCurrency() {
  $('[data-target="currency"]').each(function () {
    $(this).text(
      new Intl.NumberFormat("id", {
        style: "currency",
        currency: "IDR",
        maximumFractionDigits: 0,
      }).format(parseInt($(this).text()))
    );
  });
}

function confirmPesanan(id_mobil){
  Swal.fire({
    position: "top",
    text: "Pastikan client sudah datang dan menyerahkan ktp ke kantor yakin untuk konfirmasi pesanan?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        url: "/api/confirmPesanan",
        data: {
          id_mobil: id_mobil
          },
          success: function (data) {
            location.reload()
          }

      })
    } 
  });

}

// function confirmPesanan(status,ordeid){
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
