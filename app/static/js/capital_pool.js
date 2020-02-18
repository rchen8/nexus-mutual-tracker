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
  $('#capital-pool-size-usd').click()
})

$('#capital-pool-size-usd').click(() => {
  renderCapitalPoolSize('USD')
  toggleCurrency('#capital-pool-size', 'usd', 'eth')
})

$('#capital-pool-size-eth').click(() => {
  renderCapitalPoolSize('ETH')
  toggleCurrency('#capital-pool-size', 'eth', 'usd')
})

$.get('cover_amount_to_capital_pool_ratio', (response) => {
  Plotly.newPlot('activeCoverAmountToCapitalPoolSizeRatio', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})

$.get('minimum_capital_requirement', (response) => {
  Plotly.newPlot('minimumCapitalRequirement', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [7000, Math.max(...Object.values(response))]}
  })
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
