let capitalPoolSize = undefined
let coverAmountToCapitalPoolRatio = undefined
let minimumCapitalRequirement = undefined
let mcrPercentage = undefined

const endpoints = [
  'capital_pool_size',
  'cover_amount_to_capital_pool_ratio',
  'minimum_capital_requirement',
  'mcr_percentage'
]

Promise.all(endpoints.map(getData)).then(data => {
  capitalPoolSize = data[0]
  coverAmountToCapitalPoolRatio = data[1]
  minimumCapitalRequirement = data[2]
  mcrPercentage = data[3]

  renderStats()
  setTimeout(() => {renderGraphs()}, 0)
})

const renderStats = () => {
  $('#currentCapitalPoolSize').text(getCurrentValue(capitalPoolSize, ['USD', 'ETH']))
  $('#currentActiveCoverAmountToCapitalPoolSizeRatio')
    .text(getCurrentValue(coverAmountToCapitalPoolRatio, null).toFixed(2) + '%')
  $('#currentMinimumCapitalRequirement')
    .text(Math.round(getCurrentValue(minimumCapitalRequirement, null)).toLocaleString() + ' ETH')
  $('#currentMcrPercentage').text(getCurrentValue(mcrPercentage, null).toFixed(2) + '%')
}

const renderGraphs = () => {
  $('#capital-pool-size-usd').click()
  renderCoverAmountToCapitalPoolRatio()
  renderMinimumCapitalRequirement()
  renderMcrPercentage()
}

const renderCapitalPoolSize = (currency) => {
  Plotly.newPlot('capitalPoolSize', [{
    x: getDateTimesInLocalTimezone(Object.keys(capitalPoolSize[currency])),
    y: Object.values(capitalPoolSize[currency]),
    fill: 'tozeroy',
    type: 'scatter'
  }], {}, {responsive: true})
}

$('#capital-pool-size-usd').click(() => {
  renderCapitalPoolSize('USD')
  toggleCurrency('#capital-pool-size', 'usd', 'eth')
})

$('#capital-pool-size-eth').click(() => {
  renderCapitalPoolSize('ETH')
  toggleCurrency('#capital-pool-size', 'eth', 'usd')
})

const renderCoverAmountToCapitalPoolRatio = () => {
  Plotly.newPlot('activeCoverAmountToCapitalPoolSizeRatio', [{
    x: getDateTimesInLocalTimezone(Object.keys(coverAmountToCapitalPoolRatio)),
    y: Object.values(coverAmountToCapitalPoolRatio),
    fill: 'tozeroy',
    type: 'scatter'
  }], {}, {responsive: true})
}

const renderMinimumCapitalRequirement = () => {
  Plotly.newPlot('minimumCapitalRequirement', [{
    x: getDateTimesInLocalTimezone(Object.keys(minimumCapitalRequirement)),
    y: Object.values(minimumCapitalRequirement),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [
      7000,
      Math.max(...Object.values(minimumCapitalRequirement))
    ]}
  }, {responsive: true})
}

const renderMcrPercentage = () => {
  for (let key in mcrPercentage) {
    if (mcrPercentage[key] < 100) {
      delete mcrPercentage[key]
    }
  }

  Plotly.newPlot('mcrPercentage', [{
    x: getDateTimesInLocalTimezone(Object.keys(mcrPercentage)),
    y: Object.values(mcrPercentage),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [
      100,
      Math.max(...Object.values(mcrPercentage))
    ]}
  }, {responsive: true})
}
