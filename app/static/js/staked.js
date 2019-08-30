$.get('total_amount_staked', (response) => {
  Plotly.newPlot('totalAmountStaked', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
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
