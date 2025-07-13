// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.font.family = 'Nunito, -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.color = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
if (ctx) {
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Direct", "Referral", "Social"],
      datasets: [{
        data: [5500, 3000, 1500],
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
        hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      cutout: '80%', // replaces deprecated `cutoutPercentage`
      plugins: {
        tooltip: {
          backgroundColor: "rgb(255,255,255)",
          bodyColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          padding: 15,
          displayColors: false,
          caretPadding: 10,
          callbacks: {
            label: function (context) {
              const label = context.label || '';
              const value = context.parsed;
              return label + ': KES ' + value.toLocaleString();
            }
          }
        },
        legend: {
          display: false
        }
      }
    }
  });
}
