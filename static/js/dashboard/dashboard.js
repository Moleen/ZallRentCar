const ctx = document.getElementById("myChart");
const myChart = new Chart(ctx, {
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
        label: "Data Mobil",
        data: [30, 50, 80, 200],
        backgroundColor: [
          "rgba(255, 99, 132)", // Red
        ],
        borderColor: ["rgba(255, 99, 132, 1)"],
      },
    ],
  },
  options: {
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
      y: {
        min: 10,
        max: 50,
      },
    },
  },
});

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

$(document).ready(function () {
  changeCurrency();
});
