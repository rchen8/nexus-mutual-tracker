let nxmPrice = undefined
let nxmDailyVolume = undefined
let nxmSupply = undefined
let nxmMarketCap = undefined
let netMarketCap = undefined
let bookValueRatio = undefined
let nxmDistribution = undefined
let uniqueAddresses = undefined

const endpoints = [
  'nxm_price',
  'nxm_daily_volume',
  'nxm_supply',
  'nxm_market_cap',
  'net_market_cap',
  'book_value_ratio',
  'nxm_distribution',
  'unique_addresses'
]

Promise.all(endpoints.map(getData)).then(data => {
  nxmPrice = data[0]
  nxmDailyVolume = data[1]
  nxmSupply = data[2]
  nxmMarketCap = data[3]
  netMarketCap = data[4]
  bookValueRatio = data[5]
  nxmDistribution = data[6]
  uniqueAddresses = data[7]

  renderStats()
  setTimeout(() => {renderGraphs()}, 0)
})

const renderStats = () => {
  $('#currentNxmPrice').text(getCurrentValue(nxmPrice, ['USD', 'ETH'], true))
  $('#currentNxmSupply').text(Math.round(getCurrentValue(nxmSupply, null)).toLocaleString() + ' NXM')
  $('#currentNxmMarketCap').text(getCurrentValue(nxmMarketCap, ['USD', 'ETH']))
  $('#currentUniqueAddresses').text(getCurrentValue(uniqueAddresses, null).toLocaleString())
}

const renderGraphs = () => {
  $('#nxm-price-usd').click()
  $('#nxm-daily-volume-usd').click()
  renderNXMSupply()
  $('#nxm-market-cap-usd').click()
  $('#net-market-cap-usd').click()
  renderBookValueRatio()
  renderNXMDistribution()
  renderUniqueAddresses()
}

const renderNXMPrice = (currency) => {
  Plotly.newPlot('nxmPrice', [{
    x: Object.keys(nxmPrice[currency]),
    y: Object.values(nxmPrice[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#nxm-price-usd').click(() => {
  renderNXMPrice('USD')
  toggleCurrency('#nxm-price', 'usd', 'eth')
})

$('#nxm-price-eth').click(() => {
  renderNXMPrice('ETH')
  toggleCurrency('#nxm-price', 'eth', 'usd')
})

const renderNXMDailyVolume = (currency) => {
  Plotly.newPlot('nxmDailyVolume', [{
    x: Object.keys(nxmDailyVolume[currency]),
    y: Object.values(nxmDailyVolume[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#nxm-daily-volume-usd').click(() => {
  renderNXMDailyVolume('USD')
  toggleCurrency('#nxm-daily-volume', 'usd', 'nxm')
})

$('#nxm-daily-volume-nxm').click(() => {
  renderNXMDailyVolume('NXM')
  toggleCurrency('#nxm-daily-volume', 'nxm', 'usd')
})

const renderNXMSupply = () => {
  Plotly.newPlot('nxmSupply', [{
    x: Object.keys(nxmSupply),
    y: Object.values(nxmSupply),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {
    yaxis: {range: [
      3000000,
      Math.max(...Object.values(nxmSupply))
    ]}
  }, {responsive: true})
}

const renderNXMMarketCap = (currency) => {
  Plotly.newPlot('nxmMarketCap', [{
    x: Object.keys(nxmMarketCap[currency]),
    y: Object.values(nxmMarketCap[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#nxm-market-cap-usd').click(() => {
  renderNXMMarketCap('USD')
  toggleCurrency('#nxm-market-cap', 'usd', 'eth')
})

$('#nxm-market-cap-eth').click(() => {
  renderNXMMarketCap('ETH')
  toggleCurrency('#nxm-market-cap', 'eth', 'usd')
})

const renderNetMarketCap = (currency) => {
  Plotly.newPlot('netMarketCap', [{
    x: Object.keys(netMarketCap[currency]),
    y: Object.values(netMarketCap[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#net-market-cap-usd').click(() => {
  renderNetMarketCap('USD')
  toggleCurrency('#net-market-cap', 'usd', 'eth')
})

$('#net-market-cap-eth').click(() => {
  renderNetMarketCap('ETH')
  toggleCurrency('#net-market-cap', 'eth', 'usd')
})

const renderBookValueRatio = () => {
  Plotly.newPlot('bookValueRatio', [{
    x: Object.keys(bookValueRatio),
    y: Object.values(bookValueRatio),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

const renderNXMDistribution = () => {
  Plotly.newPlot('nxmDistribution', [{
    labels: Object.keys(nxmDistribution),
    values: Object.values(nxmDistribution),
    type: 'pie',
    textinfo: 'none'
  }], {}, {responsive: true})
}

const renderUniqueAddresses = () => {
  Plotly.newPlot('uniqueAddresses', [{
    x: Object.keys(uniqueAddresses),
    y: Object.values(uniqueAddresses),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}
