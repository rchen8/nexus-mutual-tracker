let nxmPrice = undefined
let nxmDailyVolume = undefined
let nxmMarketCap = undefined

const renderNXMPrice = (currency) => {
  if (nxmPrice !== undefined) {
    Plotly.newPlot('nxmPrice', [{
      x: getDateTimesInLocalTimezone(Object.keys(nxmPrice[currency])),
      y: Object.values(nxmPrice[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {
      yaxis: {range: [Math.min(...Object.values(nxmPrice[currency])),
          Math.max(...Object.values(nxmPrice[currency]))]}
    }, {responsive: true})
  }
}

$.get('nxm_price', (response) => {
  nxmPrice = response
  $('#currentNxmPrice').text(getCurrentValue(nxmPrice, ['USD', 'ETH'], true))
  $('#nxm-price-usd').click()
})

$('#nxm-price-usd').click(() => {
  renderNXMPrice('USD')
  toggleCurrency('#nxm-price', 'usd', 'eth')
})

$('#nxm-price-eth').click(() => {
  renderNXMPrice('ETH')
  toggleCurrency('#nxm-price', 'eth', 'usd')
})

const renderNXMDailyVolume = (currency) => {
  if (nxmDailyVolume !== undefined) {
    Plotly.newPlot('nxmDailyVolume', [{
      x: Object.keys(nxmDailyVolume[currency]),
      y: Object.values(nxmDailyVolume[currency]),
      type: 'bar'
    }], {}, {responsive: true})
  }
}

$.get('nxm_daily_volume', (response) => {
  nxmDailyVolume = response
  $('#currentNxmVolume').text(getCurrentValue(nxmDailyVolume, ['USD', 'NXM']))
  $('#nxm-daily-volume-usd').click()
})

$('#nxm-daily-volume-usd').click(() => {
  renderNXMDailyVolume('USD')
  toggleCurrency('#nxm-daily-volume', 'usd', 'nxm')
})

$('#nxm-daily-volume-nxm').click(() => {
  renderNXMDailyVolume('NXM')
  toggleCurrency('#nxm-daily-volume', 'nxm', 'usd')
})

$.get('nxm_supply', (response) => {
  $('#currentNxmSupply').text(Math.round(getCurrentValue(response, null)).toLocaleString() + ' NXM')
  Plotly.newPlot('nxmSupply', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [Math.min(...Object.values(response)), Math.max(...Object.values(response))]}
  }, {responsive: true})
})

const renderNXMMarketCap = (currency) => {
  if (nxmMarketCap !== undefined) {
    Plotly.newPlot('nxmMarketCap', [{
      x: getDateTimesInLocalTimezone(Object.keys(nxmMarketCap[currency])),
      y: Object.values(nxmMarketCap[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {
      yaxis: {range: [Math.min(...Object.values(nxmMarketCap[currency])),
          Math.max(...Object.values(nxmMarketCap[currency]))]}
    }, {responsive: true})
  }
}

$.get('nxm_market_cap', (response) => {
  nxmMarketCap = response
  $('#currentNxmMarketCap').text(getCurrentValue(nxmMarketCap, ['USD', 'ETH']))
  $('#nxm-market-cap-usd').click()
})

$('#nxm-market-cap-usd').click(() => {
  renderNXMMarketCap('USD')
  toggleCurrency('#nxm-market-cap', 'usd', 'eth')
})

$('#nxm-market-cap-eth').click(() => {
  renderNXMMarketCap('ETH')
  toggleCurrency('#nxm-market-cap', 'eth', 'usd')
})

$.get('nxm_distribution', (response) => {
  Plotly.newPlot('nxmDistribution', [{
    labels: Object.keys(response),
    values: Object.values(response),
    type: 'pie',
    textinfo: 'none'
  }], {}, {responsive: true})
})

$.get('unique_addresses', (response) => {
  $('#currentUniqueAddresses').text(getCurrentValue(response, null).toLocaleString())
  Plotly.newPlot('uniqueAddresses', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {}, {responsive: true})
})
