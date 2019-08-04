$.get('active_cover_amount', (response) => {
  Plotly.newPlot('activeCoverAmount', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})

$.get('active_cover_amount_per_contract', (response) => {
  Plotly.newPlot('activeCoverAmountPerContract', [{
    x: Object.keys(response),
    y: Object.values(response),
    type: 'bar'
  }])
})

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
  const last_mcr_percentage = Object.values(response)[Object.values(response).length - 1]
  Plotly.newPlot('mcrPercentage', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [100, last_mcr_percentage + (last_mcr_percentage - 100) / 5]}
  })
})

$.get('nxm_token_price', (response) => {
  const first_nxm_price = Object.values(response)[0]
  const last_nxm_price = Object.values(response)[Object.values(response).length - 1]
  Plotly.newPlot('nxmTokenPrice', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [first_nxm_price, last_nxm_price + (last_nxm_price - first_nxm_price) / 5]}
  })
})
