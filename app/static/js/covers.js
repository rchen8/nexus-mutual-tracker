let activeCoverAmount = undefined
let activeCoverAmountPerContract = undefined
let activeCoverAmountByExpirationDate = undefined
let premiumsPaid = undefined
let premiumsPaidPerContract = undefined
let allCovers = undefined

const endpoints = [
  'active_cover_amount',
  'active_cover_amount_per_contract',
  'active_cover_amount_by_expiration_date',
  'premiums_paid',
  'premiums_paid_per_contract',
  'all_covers'
]

Promise.all(endpoints.map(getData)).then(data => {
  activeCoverAmount = data[0]
  activeCoverAmountPerContract = data[1]
  activeCoverAmountByExpirationDate = data[2]
  premiumsPaid = data[3]
  premiumsPaidPerContract = data[4]
  allCovers = data[5]

  renderStats()
  setTimeout(() => {renderGraphs()}, 0)
})

const renderStats = () => {
  $('#currentActiveCoverAmount').text(getCurrentValue(activeCoverAmount, ['USD', 'ETH']))
  $('#currentPremiumsPaid').text(getCurrentValue(premiumsPaid, ['USD', 'ETH']))
}

const renderGraphs = () => {
  $('#active-cover-amount-usd').click()
  $('#active-cover-amount-per-contract-usd').click()
  $('#active-cover-amount-by-expiration-date-usd').click()
  $('#premiums-paid-usd').click()
  $('#premiums-paid-per-contract-usd').click()
  $('#all-covers-usd').click()
}

const renderActiveCoverAmount = (currency) => {
  Plotly.newPlot('activeCoverAmount', [{
    x: Object.keys(activeCoverAmount[currency]),
    y: Object.values(activeCoverAmount[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#active-cover-amount-usd').click(() => {
  renderActiveCoverAmount('USD')
  toggleCurrency('#active-cover-amount', 'usd', 'eth')
})

$('#active-cover-amount-eth').click(() => {
  renderActiveCoverAmount('ETH')
  toggleCurrency('#active-cover-amount', 'eth', 'usd')
})

const renderActiveCoverAmountPerContract = (currency) => {
  Plotly.newPlot('activeCoverAmountPerContract', [{
    x: Object.keys(activeCoverAmountPerContract[currency]),
    y: Object.values(activeCoverAmountPerContract[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#active-cover-amount-per-contract-usd').click(() => {
  renderActiveCoverAmountPerContract('USD')
  toggleCurrency('#active-cover-amount-per-contract', 'usd', 'eth')
})

$('#active-cover-amount-per-contract-eth').click(() => {
  renderActiveCoverAmountPerContract('ETH')
  toggleCurrency('#active-cover-amount-per-contract', 'eth', 'usd')
})

const renderActiveCoverAmountByExpirationDate = (currency) => {
  Plotly.newPlot('activeCoverAmountByExpirationDate', [{
    x: Object.keys(activeCoverAmountByExpirationDate[currency]),
    y: Object.values(activeCoverAmountByExpirationDate[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#active-cover-amount-by-expiration-date-usd').click(() => {
  renderActiveCoverAmountByExpirationDate('USD')
  toggleCurrency('#active-cover-amount-by-expiration-date', 'usd', 'eth')
})

$('#active-cover-amount-by-expiration-date-eth').click(() => {
  renderActiveCoverAmountByExpirationDate('ETH')
  toggleCurrency('#active-cover-amount-by-expiration-date', 'eth', 'usd')
})

const renderPremiumsPaid = (currency) => {
  Plotly.newPlot('premiumsPaid', [{
    x: Object.keys(premiumsPaid[currency]),
    y: Object.values(premiumsPaid[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#premiums-paid-usd').click(() => {
  renderPremiumsPaid('USD')
  toggleCurrency('#premiums-paid', 'usd', 'eth')
})

$('#premiums-paid-eth').click(() => {
  renderPremiumsPaid('ETH')
  toggleCurrency('#premiums-paid', 'eth', 'usd')
})

const renderPremiumsPaidPerContract = (currency) => {
  Plotly.newPlot('premiumsPaidPerContract', [{
    x: Object.keys(premiumsPaidPerContract[currency]),
    y: Object.values(premiumsPaidPerContract[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#premiums-paid-per-contract-usd').click(() => {
  renderPremiumsPaidPerContract('USD')
  toggleCurrency('#premiums-paid-per-contract', 'usd', 'eth')
})

$('#premiums-paid-per-contract-eth').click(() => {
  renderPremiumsPaidPerContract('ETH')
  toggleCurrency('#premiums-paid-per-contract', 'eth', 'usd')
})

const renderAllCovers = (currency) => {
  const table = $('#coverDataTable').DataTable()
  table.clear()
  for (let cover of allCovers) {
    let coverAmount = 0
    let premium = 0
    if (currency === 'USD') {
      coverAmount = '$' + cover['amount_usd'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      premium = '$' + cover['premium_usd'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    } else {
      coverAmount = cover['amount'].toLocaleString() + ' ' + cover['currency']
      premium = cover['premium'].toLocaleString() + ' ' + cover['currency']
    }

    table.row.add([
      cover['cover_id'],
      cover['contract_name'],
      coverAmount,
      premium,
      cover['start_time'],
      cover['end_time']
    ])
  }
  table.draw()
}

$('#all-covers-usd').click(() => {
  renderAllCovers('USD')
  toggleCurrency('#all-covers', 'usd', 'eth-dai')
})

$('#all-covers-eth-dai').click(() => {
  renderAllCovers('ETH/DAI')
  toggleCurrency('#all-covers', 'eth-dai', 'usd')
})
