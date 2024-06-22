import { changeCurrency } from "./function.js";

$(document).ready(function () {
  let myChart = null;

  function load_chart_pendapatan() {
    var filter = $("#filtercart").val();
    $.ajax({
      url: "/api/ambilpendapatan",
      type: "POST",
      data: {
        tahun: filter,
      },
      success: function (response) {
        let data = [];
        let total = 0;
        $.each(response, function (key, value) {
          data.push(value);
          total += value;
        });
        $("#totalPendapatan").text(total);
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
            },
          },
        });
      },
    });
  }

  load_chart_pendapatan();

  $("#filtercart").on("change", function () {
    load_chart_pendapatan();
  });
  changeCurrency();
});

$.ajax({
  type: "GET",
  url: "/api/get_transaksi",
  success: function (response) {
    let data = []
    $.each(response, function(key, value){
      data.push(value)
    })
    const ctx2 = document.getElementById("piechart");
    var myChart2 = new Chart(ctx2, {
      type: "pie",
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
            label: "transaksi",
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          datalabels: {
            anchor: "center",
            align: "center",
            formatter: (value, ctx) => {
              if (value == 0) {
                return null;
              }
              return `${ctx.chart.data.labels[ctx.dataIndex]} : ${value}`;
            },
            color: "#000",
          },
          legend: {
            display: false,
          },
        },
      },
      plugins: [ChartDataLabels],
    });
    // awsdasd
  },
});
