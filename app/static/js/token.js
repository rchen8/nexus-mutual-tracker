nxmTokenPrice = undefined

const renderNXMTokenPrice = (currency) => {
  if (nxmTokenPrice !== undefined) {
    Plotly.newPlot('nxmTokenPrice', [{
      x: getDateTimesInLocalTimezone(Object.keys(nxmTokenPrice[currency])),
      y: Object.values(nxmTokenPrice[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {
      yaxis: {range: [Math.min(...Object.values(nxmTokenPrice[currency])),
          Math.max(...Object.values(nxmTokenPrice[currency]))]}
    })
  }
}

$.get('nxm_token_price', (response) => {
  nxmTokenPrice = response
  renderNXMTokenPrice('USD')
})

$('#nxm-token-price-usd').click(() => {
  renderNXMTokenPrice('USD')
})

$('#nxm-token-price-eth').click(() => {
  renderNXMTokenPrice('ETH')
})
