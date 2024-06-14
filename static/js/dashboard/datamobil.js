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
               <li><a class="dropdown-item" onclick="confirm('pesanan','{{dt.id_mobil}}')"
                         role="button">Konfirmasi Pesanan</a></li>
                         </ul>`;
            } else if (data[i].status == "Digunakan") {
              button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" onclick="confirm('kembali','{{dt.id_mobil}}')"
                         role="button">Konfirmasi Kembali</a></li>
                         </ul>`;
            } else {
              button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" href="/data_mobil/edit?id=${data[i].id_mobil}">Edit Mobil</a></li>
               <li><a class="dropdown-item" onclick="confirm('hapus','{{dt.id_mobil}}')"
                role="button">Hapus</a></li>
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

function confirm(fitur,id_mobil) {
  doc = {
    pesanan: {
      text:
        "Pastikan client sudah datang dan menyerahkan ktp ke kantor yakin untuk konfirmasi pesanan?",
      url: "/api/confirmPesanan",
    },
    kembali: {
      text:
        "Pastikan client sudah mengembalikan mobil, yakin untuk merubah status?",
      url: "/api/confirmKembali",
    },
    hapus: {
      text: "Yakin unutk menghapus mobil?",
      url: "/api/delete_mobil",
    },
  };

  if (fitur == "pesanan") {
    text = doc.pesanan.text;
    url = doc.pesanan.url;
  } else if (fitur == "kembali") {
    text = doc.kembali.text;
    url = doc.kembali.url;
  } else if (fitur == "hapus") {
    text = doc.hapus.text;
    url = doc.hapus.url;
  }

  Swal.fire({
    position: "top",
    text: text,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        url: url,
        data: {
          id_mobil: id_mobil,
        },
        success: function (data) {
          location.reload();
        },
      });
    }
  });
}