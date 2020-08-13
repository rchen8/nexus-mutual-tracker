let activeCoverAmount = undefined
let activeCoverAmountPerContract = undefined
let activeCoverAmountByExpirationDate = undefined
let premiumsPaid = undefined
let premiumsPaidPerContract = undefined
let allCovers = undefined

const renderActiveCoverAmount = (currency) => {
  if (activeCoverAmount !== undefined) {
    Plotly.newPlot('activeCoverAmount', [{
      x: getDateTimesInLocalTimezone(Object.keys(activeCoverAmount[currency])),
      y: Object.values(activeCoverAmount[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {}, {responsive: true})
  }
}

$.get('active_cover_amount', (response) => {
  activeCoverAmount = response
  $('#currentActiveCoverAmount').text(getCurrentValue(activeCoverAmount, ['USD', 'ETH']))
  $('#active-cover-amount-usd').click()
})

$('#active-cover-amount-usd').click(() => {
  renderActiveCoverAmount('USD')
  toggleCurrency('#active-cover-amount', 'usd', 'eth')
})

$('#active-cover-amount-eth').click(() => {
  renderActiveCoverAmount('ETH')
  toggleCurrency('#active-cover-amount', 'eth', 'usd')
})

const renderActiveCoverAmountPerContract = (currency) => {
  if (activeCoverAmountPerContract !== undefined) {
    Plotly.newPlot('activeCoverAmountPerContract', [{
      x: Object.keys(activeCoverAmountPerContract[currency]),
      y: Object.values(activeCoverAmountPerContract[currency]),
      type: 'bar'
    }], {}, {responsive: true})
  }
}

$.get('active_cover_amount_per_contract', (response) => {
  activeCoverAmountPerContract = response
  $('#active-cover-amount-per-contract-usd').click()
})

$('#active-cover-amount-per-contract-usd').click(() => {
  renderActiveCoverAmountPerContract('USD')
  toggleCurrency('#active-cover-amount-per-contract', 'usd', 'eth')
})

$('#active-cover-amount-per-contract-eth').click(() => {
  renderActiveCoverAmountPerContract('ETH')
  toggleCurrency('#active-cover-amount-per-contract', 'eth', 'usd')
})

const renderActiveCoverAmountByExpirationDate = (currency) => {
  if (activeCoverAmountByExpirationDate !== undefined) {
    Plotly.newPlot('activeCoverAmountByExpirationDate', [{
      x: Object.keys(activeCoverAmountByExpirationDate[currency]),
      y: Object.values(activeCoverAmountByExpirationDate[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {}, {responsive: true})
  }
}

$.get('active_cover_amount_by_expiration_date', (response) => {
  activeCoverAmountByExpirationDate = response
  $('#active-cover-amount-by-expiration-date-usd').click()
})

$('#active-cover-amount-by-expiration-date-usd').click(() => {
  renderActiveCoverAmountByExpirationDate('USD')
  toggleCurrency('#active-cover-amount-by-expiration-date', 'usd', 'eth')
})

$('#active-cover-amount-by-expiration-date-eth').click(() => {
  renderActiveCoverAmountByExpirationDate('ETH')
  toggleCurrency('#active-cover-amount-by-expiration-date', 'eth', 'usd')
})

const renderPremiumsPaid = (currency) => {
  if (premiumsPaid !== undefined) {
    Plotly.newPlot('premiumsPaid', [{
      x: Object.keys(premiumsPaid[currency]),
      y: Object.values(premiumsPaid[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }], {}, {responsive: true})
  }
}

$.get('premiums_paid', (response) => {
  premiumsPaid = response
  $('#currentPremiumsPaid').text(getCurrentValue(premiumsPaid, ['USD', 'ETH']))
  $('#premiums-paid-usd').click()
})

$('#premiums-paid-usd').click(() => {
  renderPremiumsPaid('USD')
  toggleCurrency('#premiums-paid', 'usd', 'eth')
})

$('#premiums-paid-eth').click(() => {
  renderPremiumsPaid('ETH')
  toggleCurrency('#premiums-paid', 'eth', 'usd')
})

const renderPremiumsPaidPerContract = (currency) => {
  if (premiumsPaidPerContract !== undefined) {
    Plotly.newPlot('premiumsPaidPerContract', [{
      x: Object.keys(premiumsPaidPerContract[currency]),
      y: Object.values(premiumsPaidPerContract[currency]),
      type: 'bar'
    }], {}, {responsive: true})
  }
}

$.get('premiums_paid_per_contract', (response) => {
  premiumsPaidPerContract = response
  $('#premiums-paid-per-contract-usd').click()
})

$('#premiums-paid-per-contract-usd').click(() => {
  renderPremiumsPaidPerContract('USD')
  toggleCurrency('#premiums-paid-per-contract', 'usd', 'eth')
})

$('#premiums-paid-per-contract-eth').click(() => {
  renderPremiumsPaidPerContract('ETH')
  toggleCurrency('#premiums-paid-per-contract', 'eth', 'usd')
})

const renderAllCovers = (currency) => {
  if (allCovers !== undefined) {
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
        toLocalTimezone(cover['start_time']),
        toLocalTimezone(cover['end_time'])
      ])
    }
    table.draw()
  }
}

$.get('all_covers', (response) => {
  allCovers = response
  $('#all-covers-usd').click()
})

$('#all-covers-usd').click(() => {
  renderAllCovers('USD')
  toggleCurrency('#all-covers', 'usd', 'eth-dai')
})

$('#all-covers-eth-dai').click(() => {
  renderAllCovers('ETH/DAI')
  toggleCurrency('#all-covers', 'eth-dai', 'usd')
})
