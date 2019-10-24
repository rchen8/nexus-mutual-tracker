nxmPrice = undefined
nxmMarketCap = undefined

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
    })
  }
}

$.get('nxm_price', (response) => {
  nxmPrice = response
  renderNXMPrice('USD')
})

$('#nxm-price-usd').click(() => {
  renderNXMPrice('USD')
})

$('#nxm-price-eth').click(() => {
  renderNXMPrice('ETH')
})

$.get('nxm_supply', (response) => {
  Plotly.newPlot('nxmSupply', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [Math.min(...Object.values(response)), Math.max(...Object.values(response))]}
  })
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
    })
  }
}

$.get('nxm_market_cap', (response) => {
  nxmMarketCap = response
  renderNXMMarketCap('USD')
})

$('#nxm-market-cap-usd').click(() => {
  renderNXMMarketCap('USD')
})

$('#nxm-market-cap-eth').click(() => {
  renderNXMMarketCap('ETH')
})

$.get('nxm_distribution', (response) => {
  Plotly.newPlot('nxmDistribution', [{
    labels: Object.keys(response),
    values: Object.values(response),
    type: 'pie',
    hoverinfo: 'label+percent',
    textinfo: 'none'
  }])
})
