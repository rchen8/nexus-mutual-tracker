$.get('capital_pool_size', (response) => {
  Plotly.newPlot('capitalPoolSize', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})

$.get('capital_pool_distribution', (response) => {
  Plotly.newPlot('capitalPoolDistribution', [{
    labels: Object.keys(response),
    values: Object.values(response),
    type: 'pie',
    hoverinfo: 'label+percent',
    textinfo: 'none'
  }])
})

$.get('mcr_percentage', (response) => {
  Plotly.newPlot('mcrPercentage', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [100, Math.max(...Object.values(response))]}
  })
})
