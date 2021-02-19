let activeCoverAmount = undefined
let activeCoverAmountPerProject = undefined
let activeCoverAmountByExpirationDate = undefined
let defiTvlCovered = undefined
let annualizedPremiumsInForce = undefined
let totalPremiumsPaid = undefined
let premiumsPaidPerProject = undefined
let monthlySurplus = undefined
let allCovers = undefined

const endpoints = [
  'active_cover_amount',
  'active_cover_amount_per_project',
  'active_cover_amount_by_expiration_date',
  'defi_tvl_covered',
  'annualized_premiums_in_force',
  'total_premiums_paid',
  'premiums_paid_per_project',
  'monthly_surplus',
  'all_covers'
]

Promise.all(endpoints.map(getData)).then(data => {
  activeCoverAmount = data[0]
  activeCoverAmountPerProject = data[1]
  activeCoverAmountByExpirationDate = data[2]
  defiTvlCovered = data[3]
  annualizedPremiumsInForce = data[4]
  totalPremiumsPaid = data[5]
  premiumsPaidPerProject = data[6]
  monthlySurplus = data[7]
  allCovers = data[8]

  renderStats()
  setTimeout(() => {renderGraphs()}, 0)
})

const renderStats = () => {
  $('#currentActiveCoverAmount').text(getCurrentValue(activeCoverAmount, ['USD', 'ETH']))
  $('#currentAnnualizedPremiumsInForce').text(
      getCurrentValue(annualizedPremiumsInForce, ['USD', 'ETH']))
}

const renderGraphs = () => {
  $('#active-cover-amount-usd').click()
  $('#active-cover-amount-per-project-usd').click()
  $('#active-cover-amount-by-expiration-date-usd').click()
  renderDefiTvlCovered()
  $('#annualized-premiums-in-force-usd').click()
  $('#total-premiums-paid-usd').click()
  $('#premiums-paid-per-project-usd').click()
  $('#monthly-surplus-usd').click()
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

const renderActiveCoverAmountPerProject = (currency) => {
  Plotly.newPlot('activeCoverAmountPerProject', [{
    x: Object.keys(activeCoverAmountPerProject[currency]),
    y: Object.values(activeCoverAmountPerProject[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#active-cover-amount-per-project-usd').click(() => {
  renderActiveCoverAmountPerProject('USD')
  toggleCurrency('#active-cover-amount-per-project', 'usd', 'eth')
})

$('#active-cover-amount-per-project-eth').click(() => {
  renderActiveCoverAmountPerProject('ETH')
  toggleCurrency('#active-cover-amount-per-project', 'eth', 'usd')
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

const renderDefiTvlCovered = () => {
  Plotly.newPlot('defiTvlCovered', [{
    x: Object.keys(defiTvlCovered),
    y: Object.values(defiTvlCovered),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

const renderAnnualizedPremiumsInForce = (currency) => {
  Plotly.newPlot('annualizedPremiumsInForce', [{
    x: Object.keys(annualizedPremiumsInForce[currency]),
    y: Object.values(annualizedPremiumsInForce[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#annualized-premiums-in-force-usd').click(() => {
  renderAnnualizedPremiumsInForce('USD')
  toggleCurrency('#annualized-premiums-in-force', 'usd', 'eth')
})

$('#annualized-premiums-in-force-eth').click(() => {
  renderAnnualizedPremiumsInForce('ETH')
  toggleCurrency('#annualized-premiums-in-force', 'eth', 'usd')
})

const renderTotalPremiumsPaid = (currency) => {
  Plotly.newPlot('totalPremiumsPaid', [{
    x: Object.keys(totalPremiumsPaid[currency]),
    y: Object.values(totalPremiumsPaid[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#total-premiums-paid-usd').click(() => {
  renderTotalPremiumsPaid('USD')
  toggleCurrency('#total-premiums-paid', 'usd', 'eth')
})

$('#total-premiums-paid-eth').click(() => {
  renderTotalPremiumsPaid('ETH')
  toggleCurrency('#total-premiums-paid', 'eth', 'usd')
})

const renderPremiumsPaidPerProject = (currency) => {
  Plotly.newPlot('premiumsPaidPerProject', [{
    x: Object.keys(premiumsPaidPerProject[currency]),
    y: Object.values(premiumsPaidPerProject[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#premiums-paid-per-project-usd').click(() => {
  renderPremiumsPaidPerProject('USD')
  toggleCurrency('#premiums-paid-per-project', 'usd', 'eth')
})

$('#premiums-paid-per-project-eth').click(() => {
  renderPremiumsPaidPerProject('ETH')
  toggleCurrency('#premiums-paid-per-project', 'eth', 'usd')
})

const renderMonthlySurplus = (currency) => {
  Plotly.newPlot('monthlySurplus', [{
    x: Object.keys(monthlySurplus[currency]),
    y: Object.values(monthlySurplus[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#monthly-surplus-usd').click(() => {
  renderMonthlySurplus('USD')
  toggleCurrency('#monthly-surplus', 'usd', 'eth')
})

$('#monthly-surplus-eth').click(() => {
  renderMonthlySurplus('ETH')
  toggleCurrency('#monthly-surplus', 'eth', 'usd')
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
      cover['project'],
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
