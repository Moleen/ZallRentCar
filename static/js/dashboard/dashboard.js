$("#loading").show();



function loadChart() {

}

function changeCurrency() {
  $('[data-target="currency"]').each(function () {
    var currentText = $(this).text().trim();
    console.log(currentText);
    if(currentText.includes("Rp")){
      return
    }else{
      $(this).text(
        new Intl.NumberFormat("id", {
          style: "currency",
          currency: "IDR",
          maximumFractionDigits: 0,
        }).format(parseInt($(this).text()))
      );
    }

    });
}



$(document).ready(function () {
  let myChart = null;

  function load_chart(){
    var filter = $('#filtercart').val();
    $.ajax({
      url: "/api/ambilpendapatan",
      type: "POST",
      data: {
        tahun : filter
      },
      success: function (response) {

        let data = [];
        total = 0
        $.each(response, function (key, value) {
          data.push(value);
          total += value
        });
        $('#totalPendapatan').text(total)
        changeCurrency();
        if (myChart) {
          myChart.destroy();
        }

        const ctx = document.getElementById("myChart");
        myChart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: [
              "Januari",
              "Februari",
              "Maret",
              "April",
              "Mei",
              "Juni",
              "Juli",
              "Agustus",
              "September",
              "Oktober",
              "November",
              "Desember",
            ],
            datasets: [
              {
                label: "Pendapatan",
                data: data,
                backgroundColor: [
                  "rgba(255, 99, 132)", // Red
                ],
                borderColor: ["rgba(255, 99, 132, 1)"],
                borderRadius: 20,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false,
              },
            },
            scales: {
              x: {
                grid: {
                  display: false,
                },
              },
              // y: {
              //   min: 1000,
              //   max: 200000,
              // },
            },
          },
        });
      },
    });
  }

  load_chart()

  $('#filtercart').on('change', function(){
    load_chart();
  })
  changeCurrency();
});
