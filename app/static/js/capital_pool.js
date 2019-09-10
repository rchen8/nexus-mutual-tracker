capitalPoolSize = undefined

const renderCapitalPoolSize = (currency) => {
  if (capitalPoolSize !== undefined) {
    Plotly.newPlot('capitalPoolSize', [{
      x: getDateTimesInLocalTimezone(Object.keys(capitalPoolSize[currency])),
      y: Object.values(capitalPoolSize[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }])
  }
}

$.get('capital_pool_size', (response) => {
  capitalPoolSize = response
  renderCapitalPoolSize('USD')
})

$('#capital-pool-size-usd').click(() => {
  renderCapitalPoolSize('USD')
})

$('#capital-pool-size-eth').click(() => {
  renderCapitalPoolSize('ETH')
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
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [100, Math.max(...Object.values(response))]}
  })
})
