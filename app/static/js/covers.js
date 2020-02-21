let activeCoverAmount = undefined
let activeCoverAmountPerContract = undefined
let activeCoverAmountByExpirationDate = undefined
let averageCoverAmount = undefined
let allCovers = undefined

const renderActiveCoverAmount = (currency) => {
  if (activeCoverAmount !== undefined) {
    Plotly.newPlot('activeCoverAmount', [{
      x: getDateTimesInLocalTimezone(Object.keys(activeCoverAmount[currency])),
      y: Object.values(activeCoverAmount[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }])
  }
}

$.get('active_cover_amount', (response) => {
  activeCoverAmount = response
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
    }])
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
    }])
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

const renderAverageCoverAmount = (currency) => {
  if (averageCoverAmount !== undefined) {
    Plotly.newPlot('averageCoverAmount', [{
      x: Object.keys(averageCoverAmount[currency]),
      y: Object.values(averageCoverAmount[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }])
  }
}

$.get('average_cover_amount', (response) => {
  averageCoverAmount = response
  $('#average-cover-amount-usd').click()
})

$('#average-cover-amount-usd').click(() => {
  renderAverageCoverAmount('USD')
  toggleCurrency('#average-cover-amount', 'usd', 'eth')
})

$('#average-cover-amount-eth').click(() => {
  renderAverageCoverAmount('ETH')
  toggleCurrency('#average-cover-amount', 'eth', 'usd')
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
