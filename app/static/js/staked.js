totalAmountStaked = undefined
amountStakedPerContract = undefined

const renderTotalAmountStaked = (currency) => {
  if (totalAmountStaked !== undefined) {
    Plotly.newPlot('totalAmountStaked', [{
      x: getDateTimesInLocalTimezone(Object.keys(totalAmountStaked[currency])),
      y: Object.values(totalAmountStaked[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }])
  }
}

$.get('total_amount_staked', (response) => {
  totalAmountStaked = response
  renderTotalAmountStaked('USD')
})

$('#total-amount-staked-usd').click(() => {
  renderTotalAmountStaked('USD')
})

$('#total-amount-staked-nxm').click(() => {
  renderTotalAmountStaked('NXM')
})

const renderAmountStakedPerContract = (currency) => {
  if (amountStakedPerContract !== undefined) {
    Plotly.newPlot('amountStakedPerContract', [{
      x: Object.keys(amountStakedPerContract[currency]),
      y: Object.values(amountStakedPerContract[currency]),
      type: 'bar'
    }])
  }
}

$.get('amount_staked_per_contract', (response) => {
  amountStakedPerContract = response
  renderAmountStakedPerContract('USD')
})

$('#amount-staked-per-contract-usd').click(() => {
  renderAmountStakedPerContract('USD')
})

$('#amount-staked-per-contract-nxm').click(() => {
  renderAmountStakedPerContract('NXM')
})
