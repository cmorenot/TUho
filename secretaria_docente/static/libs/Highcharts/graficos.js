



Highcharts.chart('gestor', {

  title: {
      text: 'Gestores',
      align: 'left'
  },

  subtitle: {
      text: 'Rendimiento por Gestor',
      align: 'left'
  },

  yAxis: {
      title: {
          text: 'Trámites procesados'
      }
  },

  xAxis: {
      accessibility: {
          rangeDescription: 'Range: 2010 to 2020'
      }
  },

  legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle'
  },

  plotOptions: {
      series: {
          label: {
              connectorAllowed: false
          },
          pointStart: 2010
      }
  },

  series: [{
      name: 'Gestor 1 NOMBRE',
      data: [
          43934, 48656, 65165, 81827, 112143, 142383,
          171533, 165174, 155157, 161454, 154610
      ]
  }, {
      name: 'Gestor 2 NOMBRE',
      data: [
          24916, 37941, 29742, 29851, 32490, 30282,
          38121, 36885, 33726, 34243, 31050
      ]
  }, {
      name: 'Gestor 3 NOMBRE ',
      data: [
          11744, 30000, 16005, 19771, 20185, 24377,
          32147, 30912, 29243, 29213, 25663
      ]
  }, {
      name: 'Gestor 4 NOMBRE',
      data: [
          null, null, null, null, null, null, null,
          null, 11164, 11218, 10077
      ]
  }, {
      name: 'Gestor 5 NOMBRE',
      data: [
          21908, 5548, 8105, 11248, 8989, 11816, 18274,
          17300, 13053, 11906, 10073
      ]
  }],

  responsive: {
      rules: [{
          condition: {
              maxWidth: 500
          },
          chartOptions: {
              legend: {
                  layout: 'horizontal',
                  align: 'center',
                  verticalAlign: 'bottom'
              }
          }
      }]
  }

});


// Create the chart

// Data retrieved from https://netmarketshare.com/
// Build the chart
Highcharts.chart('estados', {
  chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie'
  },
  title: {
      text: 'Estados de los trámites',
      align: 'left'
  },
  tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
  },
  accessibility: {
      point: {
          valueSuffix: '%'
      }
  },
  plotOptions: {
      pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
              enabled: false
          },
          showInLegend: true
      }
  },
  series: [{
      name: 'Total',
      colorByPoint: true,
      data: [{
          name: 'Espera',
          y: 74.77,
          sliced: true,
          selected: true
      },  {
          name: 'Aceptado',
          y: 12.82
      },  {
          name: 'Rechazado',
          y: 4.63
      }, {
          name: 'Procesando',
          y: 2.44
      }, {
          name: 'Listo para recoger',
          y: 2.02
      }, {
          name: 'Entregado',
          y: 3.28
      },{
        name: 'Completado',
        y: 3.28
    }]
  }]
});






const chart = Highcharts.chart('prueba4', {
    title: {
        text: 'Tipos de Trámites ',
        align: 'left'
    },
    subtitle: {
        text: 'Chart option: Plain | Source: ' +
            '<a href="https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/helt-ledige"' +
            'target="_blank">NAV</a>',
        align: 'left'
    },
    colors: [
        '#4caefe',
        '#3fbdf3',
        '#35c3e8',
        '#2bc9dc',
        '#20cfe1',
        '#16d4e6',
        '#0dd9db',
        '#03dfd0',
        '#00e4c5',
        '#00e9ba',
        '#00eeaf',
        '#23e274'
    ],
    xAxis: {
        categories: [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec'
        ]
    },
    series: [{
        type: 'column',
        name: 'Unemployed',
        borderRadius: 5,
        colorByPoint: true,
        data: [
            5412, 4977, 4730, 4437, 3947, 3707, 4143, 3609,
            3311, 3072, 2899, 2887
        ],
        showInLegend: false
    }]
});

document.getElementById('plain').addEventListener('click', () => {
    chart.update({
        chart: {
            inverted: false,
            polar: false
        },
        subtitle: {
            text: 'Chart option: Plain | Source: ' +
                '<a href="https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/helt-ledige"' +
                'target="_blank">NAV</a>'
        }
    });
});

document.getElementById('inverted').addEventListener('click', () => {
    chart.update({
        chart: {
            inverted: true,
            polar: false
        },
        subtitle: {
            text: 'Chart option: Inverted | Source: ' +
                '<a href="https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/helt-ledige"' +
                'target="_blank">NAV</a>'
        }
    });
});

document.getElementById('polar').addEventListener('click', () => {
    chart.update({
        chart: {
            inverted: false,
            polar: true
        },
        subtitle: {
            text: 'Chart option: Polar | Source: ' +
                '<a href="https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/helt-ledige"' +
                'target="_blank">NAV</a>'
        }
    });
});


