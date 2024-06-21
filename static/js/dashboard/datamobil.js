import { addStatusLabel, changeCurrency } from "./function.js";

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
             var button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" onclick="confirm('pesanan','{{dt.id_mobil}}')"
                         role="button">Konfirmasi Pesanan</a></li>
                         </ul>`;
            } else if (data[i].status == "Digunakan") {
             var button = `<ul class="dropdown-menu">
               <li><a class="dropdown-item" onclick="confirm('kembali','{{dt.id_mobil}}')"
                         role="button">Konfirmasi Kembali</a></li>
                         </ul>`;
            } else {
             var button = `<ul class="dropdown-menu">
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

export function confirm(fitur, id_mobil) {
  let doc = {
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
    var text = doc.pesanan.text;
    var url = doc.pesanan.url;
  } else if (fitur == "kembali") {
    var text = doc.kembali.text;
    var url = doc.kembali.url;
  } else if (fitur == "hapus") {
    var text = doc.hapus.text;
    var url = doc.hapus.url;
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
        success: function (response) {
          if(response['result'] == 'unsuccess'){
            toastr.warning(response['msg'])
            console.log('tres');
          }else{
            location.reload();
          }
        },
      });
    }
  });
}

window.confirm = confirm;