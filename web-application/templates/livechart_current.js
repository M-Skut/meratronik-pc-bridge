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
          label: 'Current',
          data: {{ amp_data | tojson }},
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#ff006f',
          borderWidth: 4,
          pointBackgroundColor: '#ff006f',
          yAxisID: 'amp_axis',
      }]
    },
    options: {
      scales: {
        amp_axis: {
          type: 'linear',
          display: true,
          position: 'right',
          ticks: {
            callback: function(value, index, values) {
              return value + ' A';
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

