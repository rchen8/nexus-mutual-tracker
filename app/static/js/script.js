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
  Plotly.newPlot('mcrPercentage', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [100, Math.max(...Object.values(response))]}
  })
})

$.get('total_amount_staked', (response) => {
  Plotly.newPlot('totalAmountStaked', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})

$.get('amount_staked_per_contract', (response) => {
  Plotly.newPlot('amountStakedPerContract', [{
    x: Object.keys(response),
    y: Object.values(response),
    type: 'bar'
  }])
})

$.get('nxm_token_price', (response) => {
  Plotly.newPlot('nxmTokenPrice', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }], {
    yaxis: {range: [Math.min(...Object.values(response)), Math.max(...Object.values(response))]}
  })
})
