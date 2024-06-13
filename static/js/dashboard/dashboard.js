

function logout() {
  $.removeCookie("token", { path: "/" });
  window.location.reload();
}

function hideSidebar() {
  $(".logo h4").toggleClass("d-none");
  $(this).toggle(function () {
    $("body").css("grid-template-columns", "5rem 1fr 1fr");
  });
}



// list mobil

$(document).ready(function () {
  addStatusLabel();
  changeCurrency();

  // Function to fetch and display the car data
  function fetchCarData() {
    $.ajax({
      url: "/api/daftar_mobil",
      type: "GET",
      success: function (data) {
        $("#list-mobil").empty();
        if (data.data_mobil.length === 0) {
          var temp = "<div class='col-12 text-center'>No Data</div>";
          $("#list-mobil").append(temp);
        } else {
          data.data_mobil.forEach(function (mobil, index) {
            var temp = `<div class="card-mobil">
                <div class="card-body p-4">
                    <h3 class="card-title mb-4">${mobil.merek}</h3>
                    <img src="static/gambar/${mobil.gambar}" alt="${mobil.gambar}" class="rounded card-image mb-4">
                    <div class="d-flex flex-column align-items-center">
                        <ul class="list-detail m-0 p-0 py-4 w-75">
                            <li class="d-flex"><img src="static/icon/car-seat-icon.svg">${mobil.seat}</li>
                            <li class="d-flex"><img src="static/icon/manual-transmission-icon.svg">${mobil.transmisi}</li>
                            <li class="d-flex ms-auto" data-target="currency">${mobil.harga}</li>
                        </ul>
                        <a class="btn car-btn btn-primary m-auto w-75" href="/detail-mobil?id=${mobil.id_mobil}">Detail</a>
                    </div>
                </div>
            </div>`;
            $("#list-mobil").append(temp);
          });
        }
        addStatusLabel();
        changeCurrency();
      }
    });
  }

  fetchCarData(); // Call function on document ready

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
});


const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Data Mobil', 'Transaksi', 'Customer', 'Pendapatan Setahun'],
        datasets: [{
            label: 'Data',
            data: [30, 50, 80, 100],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)', // Red
                'rgba(54, 162, 235, 0.2)', // Blue
                'rgba(75, 192, 192, 0.2)', // Green
                'rgba(153, 102, 255, 0.2)' // Purple
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});