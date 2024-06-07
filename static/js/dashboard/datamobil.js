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
            var temp = `<tr>
                   <td>${i + 1}</td>
                   <td id="merek">${data[i].merek}</td>
                   <td>${data[i].seat}</td>
                   <td>${data[i].transmisi}</td>
                   <td data-target="currency">${data[i].harga}</td>
                   <td id="status">${data[i].status}</td>
                   <td>
                   <button class="btn fa-solid fa-ellipsis" type="button" data-bs-toggle="dropdown"
                     aria-expanded="false"></button>
                   <ul class="dropdown-menu">
                     {% if dt.status == 'Diproses' %}
                     <li><a class="dropdown-item" onclick="changeStatus('{{dt.status}}','{{dt.order_id}}')"
                         role="button">Konfirmasi Pesanan</a></li>
                     {% elif dt.status == 'Digunakan' %}
                     <li><a class="dropdown-item" onclick="changeStatus('{{dt.status}}','{{dt.order_id}}')"
                         role="button">Konfirmasi Kembali</a></li>
                     {% else %}
       
                     <li><a class="dropdown-item" href="#">Edit Mobil</a></li>
                     {% endif %}
                   </ul>
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
