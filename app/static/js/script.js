$.get('cover_amount_over_time', (response) => {
  Plotly.newPlot('coverAmountOverTime', [
    {
      x: Object.keys(response),
      y: Object.values(response),
      fill: 'tozeroy',
      type: 'scatter'
    }
  ])
})

$.get('cover_amount_per_contract', (response) => {
  Plotly.newPlot('coverAmountPerContract', [
    {
      x: Object.keys(response),
      y: Object.values(response),
      type: 'bar'
    }
  ])
})
