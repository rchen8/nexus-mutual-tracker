let allClaims = undefined
let allVotes = undefined

const renderAllClaims = (currency) => {
  if (allClaims !== undefined) {
    const table = $('#claimDataTable').DataTable()
    table.clear()
    for (let claim of allClaims) {
      let claimAmount = 0
      if (currency === 'USD') {
        claimAmount = '$' + claim['amount_usd'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      } else {
        claimAmount = claim['amount'].toLocaleString() + ' ' + claim['currency']
      }

      table.row.add([
        claim['claim_id'],
        claim['cover_id'],
        claim['contract_name'],
        claimAmount,
        claim['start_time'],
        claim['timestamp'],
        claim['verdict']
      ])
    }
    table.draw()
  }
}

$.get('all_claims', (response) => {
  allClaims = response
  $('#all-claims-usd').click()
})

$('#all-claims-usd').click(() => {
  renderAllClaims('USD')
  toggleCurrency('#all-claims', 'usd', 'eth-dai')
})

$('#all-claims-eth-dai').click(() => {
  renderAllClaims('ETH/DAI')
  toggleCurrency('#all-claims', 'eth-dai', 'usd')
})

const renderAllVotes = (currency) => {
  let values = []
  Object.values(allVotes[currency]).forEach((value) => {
    values.push(value['Yes'])
  })
  const yes = {
    x: values,
    y: Object.keys(allVotes[currency]),
    name: 'Yes',
    orientation: 'h',
    type: 'bar'
  };

  values = []
  Object.values(allVotes[currency]).forEach((value) => {
    values.push(value['No'])
  })
  const no = {
    x: values,
    y: Object.keys(allVotes[currency]),
    name: 'No',
    orientation: 'h',
    type: 'bar',
  };

  Plotly.newPlot('allVotes',
    [yes, no],
    {height: 30 * Object.keys(allVotes[currency]).length},
    {responsive: true}
  );
}

$.get('all_votes', (response) => {
  allVotes = response
  $('#all-votes-usd').click()
})

$('#all-votes-usd').click(() => {
  renderAllVotes('USD')
  toggleCurrency('#all-votes', 'usd', 'nxm')
})

$('#all-votes-nxm').click(() => {
  renderAllVotes('NXM')
  toggleCurrency('#all-votes', 'nxm', 'usd')
})
