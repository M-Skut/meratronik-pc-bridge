(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  const config = {
    type: 'line',
    data: {
      labels: {{ timestamps | tojson }},
      datasets: [{
          label: 'Voltage',
          data: {{ volt_data | tojson }},
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#ff006f',
          borderWidth: 4,
          pointBackgroundColor: '#ff006f',
          yAxisID: 'volt_axis',
      }]
    },
    options: {
      scales: {
        volt_axis: {
          type: 'linear',
          display: true,
          position: 'right',
          ticks: {
            callback: function(value, index, values) {
              return value + ' V';
            }
          }
        },
        x: {
          type: 'time'
        }
      },
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  }
var lineChart = new Chart(ctx, config)

}) ()

