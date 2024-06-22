import { addStatusLabel, changeCurrency } from "./function.js";

$(document).ready(function () {
  addStatusLabel();
  changeCurrency();
});


$("#filter_transaksi").on("change", function () {
  $("#tanggal_input").remove();
  var filter = $(this).val();

  if (filter == "1") {
    $("#tanggal").attr("hidden", false);
    $("#tanggal").append('<input type="text" readonly id="tanggal_input">');
    $("#tanggal_input").datepicker({
      dateFormat: "dd-MM-yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2100",
    });

    $("#tanggal_input").on("change", function () {
      $(this).prop("disabled", true);
      $.ajax({
        type: "POST",
        url: "/api/filter_transaksi",
        data: {
          mtd: "fTanggal",
          date: $(this).val(),
        },
        success: function (response) {
          $("#list-data").empty();
          

          if (response.length == 0) {
            $("#list-data").append(
              "<tr><td colspan='8' class='text-center'>Tidak ada transaksi</td></tr>"
            );
          } else {
            for (let i = 0; i < response.length; i++) {
              var temp = `<tr>
                                <td>${i + 1}</th>
                                <td>${response[i].item}</td>
                                <td>${response[i].penyewa}</td>
                                <td>${response[i].lama_rental}</td>
                                <td data-target="currency">${
                                  response[i].total
                                }</td>
                                <td>${response[i].date_rent}</td>
                                <td>${response[i].end_rent}</td>
                                <td id="status">${response[i].status}</td>
                           </tr>`;

              $("#list-data").append(temp);
            }
            
            addStatusLabel();
            changeCurrency();
          }
        },
      });
      $(this).prop("disabled", false);
    });
  } else if (filter == "2") {
    $.ajax({
      type: "POST",
      url: "/api/filter_transaksi",
      data: {
        mtd: "fPaid",
        date: $(this).val(),
      },
      success: function (response) {
        $("#list-data").empty();
        if (response.length == 0) {
          $("#list-data").append(
            "<tr><td colspan='8' class='text-center'>Tidak ada transaksi</td></tr>"
          );
        } else {
          for (let i = 0; i < response.length; i++) {
            var temp = `<tr>
                                <td>${i + 1}</th>
                                <td>${response[i].item}</td>
                                <td>${response[i].penyewa}</td>
                                <td>${response[i].lama_rental}</td>
                                <td data-target="currency">${
                                  response[i].total
                                }</td>
                                <td>${response[i].date_rent}</td>
                                <td>${response[i].end_rent}</td>
                                <td id="status">${response[i].status}</td>
                           </tr>`;

            $("#list-data").append(temp);
          }
          $(this).prop("disabled", false);
          addStatusLabel();
          changeCurrency();
        }
      },
    });
  } else if (filter == "3") {
    $.ajax({
      type: "POST",
      url: "/api/filter_transaksi",
      data: {
        mtd: "fUnpaid",
        date: $(this).val(),
      },
      success: function (response) {
        $("#list-data").empty();
        if (response.length == 0) {
          $("#list-data").append(
            "<tr><td colspan='8' class='text-center'>Tidak ada transaksi</td></tr>"
          );
        } else {
          for (let i = 0; i < response.length; i++) {
            var temp = `<tr>
                                <td>${i + 1}</th>
                                <td>${response[i].item}</td>
                                <td>${response[i].penyewa}</td>
                                <td>${response[i].lama_rental}</td>
                                <td data-target="currency">${
                                  response[i].total
                                }</td>
                                <td>${response[i].date_rent}</td>
                                <td>${response[i].end_rent}</td>
                                <td id="status">${response[i].status}</td>
                           </tr>`;

            $("#list-data").append(temp);
          }
          $(this).prop("disabled", false);
          addStatusLabel();
          changeCurrency();
        }
      },
    });
  }
});
