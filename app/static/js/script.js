$.get('active_cover_amount_over_time', (response) => {
  Plotly.newPlot('activeCoverAmountOverTime', [{
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

$.get('capital_pool_size_over_time', (response) => {
  Plotly.newPlot('capitalPoolSizeOverTime', [{
    x: Object.keys(response),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})
