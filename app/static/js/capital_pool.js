capitalPoolSize = undefined

const renderCapitalPoolSize = (currency) => {
  if (capitalPoolSize !== undefined) {
    Plotly.newPlot('capitalPoolSize', [{
      x: getDateTimesInLocalTimezone(Object.keys(capitalPoolSize[currency])),
      y: Object.values(capitalPoolSize[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {}, {responsive: true})
  }
}

$.get('capital_pool_size', (response) => {
  capitalPoolSize = response
  $('#currentCapitalPoolSize').text(getCurrentValue(capitalPoolSize, ['USD', 'ETH']))
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
  $('#currentActiveCoverAmountToCapitalPoolSizeRatio').text(
      getCurrentValue(response, null).toFixed(2) + '%')
  Plotly.newPlot('activeCoverAmountToCapitalPoolSizeRatio', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {}, {responsive: true})
})

$.get('minimum_capital_requirement', (response) => {
  $('#currentMinimumCapitalRequirement').text(
      Math.round(getCurrentValue(response, null)).toLocaleString() + ' ETH')
  Plotly.newPlot('minimumCapitalRequirement', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [7000, Math.max(...Object.values(response))]}
  }, {responsive: true})
})

$.get('mcr_percentage', (response) => {
  for (let key in response) {
    if (response[key] < 100) {
      delete response[key]
    }
  }

  $('#currentMcrPercentage').text(getCurrentValue(response, null).toFixed(2) + '%')
  Plotly.newPlot('mcrPercentage', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [100, Math.max(...Object.values(response))]}
  }, {responsive: true})
})
