let capitalPoolSize = undefined
let capitalEfficiencyRatio = undefined
let minimumCapitalRequirement = undefined
let mcrPercentage = undefined

const endpoints = [
  'capital_pool_size',
  'capital_efficiency_ratio',
  'minimum_capital_requirement',
  'mcr_percentage',
  'current_mcr_percentage'
]

Promise.all(endpoints.map(getData)).then(data => {
  capitalPoolSize = data[0]
  capitalEfficiencyRatio = data[1]
  minimumCapitalRequirement = data[2]
  mcrPercentage = data[3]

  renderStats(data[4])
  setTimeout(() => {renderGraphs()}, 0)
})

const renderStats = (currentMcrPercentage) => {
  $('#currentCapitalPoolSize').text(getCurrentValue(capitalPoolSize, ['USD', 'ETH']))
  $('#currentCapitalEfficiencyRatio')
    .text(getCurrentValue(capitalEfficiencyRatio, null).toFixed(2) + '%')
  $('#currentMinimumCapitalRequirement')
    .text(Math.round(getCurrentValue(minimumCapitalRequirement, null)).toLocaleString() + ' ETH')
  $('#currentMcrPercentage').text(currentMcrPercentage.toFixed(2) + '%')
}

const renderGraphs = () => {
  $('#capital-pool-size-usd').click()
  renderCapitalEfficiencyRatio()
  renderMinimumCapitalRequirement()
  renderMcrPercentage()
}

const renderCapitalPoolSize = (currency) => {
  Plotly.newPlot('capitalPoolSize', [{
    x: Object.keys(capitalPoolSize[currency]),
    y: Object.values(capitalPoolSize[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
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

const renderCapitalEfficiencyRatio = () => {
  Plotly.newPlot('capitalEfficiencyRatio', [{
    x: Object.keys(capitalEfficiencyRatio),
    y: Object.values(capitalEfficiencyRatio),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

const renderMinimumCapitalRequirement = () => {
  Plotly.newPlot('minimumCapitalRequirement', [{
    x: Object.keys(minimumCapitalRequirement),
    y: Object.values(minimumCapitalRequirement),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {
    yaxis: {range: [
      7000,
      Math.max(...Object.values(minimumCapitalRequirement)) * 1.01
    ]}
  }, {responsive: true})
}

const renderMcrPercentage = () => {
  for (let key in mcrPercentage) {
    if (mcrPercentage[key] < 100) {
      delete mcrPercentage[key]
    } else {
      break
    }
  }

  Plotly.newPlot('mcrPercentage', [{
    x: Object.keys(mcrPercentage),
    y: Object.values(mcrPercentage),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {
    yaxis: {range: [
      Math.min(...Object.values(mcrPercentage)) * 0.99,
      Math.max(...Object.values(mcrPercentage)) * 1.01
    ]}
  }, {responsive: true})
}
