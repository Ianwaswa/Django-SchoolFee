// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.font.family = 'Nunito, -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.color = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };

  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
if (ctx) {
  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["January", "February", "March", "April", "May", "June"],
      datasets: [{
        label: "Revenue",
        backgroundColor: "#4e73df",
        hoverBackgroundColor: "#2e59d9",
        borderColor: "#4e73df",
        data: [4215, 5312, 6251, 7841, 9821, 14984],
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        x: {
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 6
          },
          maxBarThickness: 25
        },
        y: {
          min: 0,
          max: 15000,
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
            callback: function(value) {
              return '$' + number_format(value);
            }
          },
          grid: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          titleMarginBottom: 10,
          titleFont: {
            size: 14
          },
          titleColor: '#6e707e',
          bodyColor: '#858796',
          backgroundColor: "rgb(255,255,255)",
          borderColor: '#dddfeb',
          borderWidth: 1,
          padding: 15,
          displayColors: false,
          caretPadding: 10,
          callbacks: {
            label: function(context) {
              var label = context.dataset.label || '';
              return label + ': $' + number_format(context.parsed.y);
            }
          }
        }
      }
    }
  });
}
