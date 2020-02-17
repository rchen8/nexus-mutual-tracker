totalAmountStaked = undefined
amountStakedPerContract = undefined
totalStakingReward = undefined
stakingRewardPerContract = undefined
allStakes = undefined

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
  $('#total-amount-staked-usd').click()
})

$('#total-amount-staked-usd').click(() => {
  renderTotalAmountStaked('USD')
  toggleCurrency('#total-amount-staked', 'usd', 'nxm')
})

$('#total-amount-staked-nxm').click(() => {
  renderTotalAmountStaked('NXM')
  toggleCurrency('#total-amount-staked', 'nxm', 'usd')
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
  $('#amount-staked-per-contract-usd').click()
})

$('#amount-staked-per-contract-usd').click(() => {
  renderAmountStakedPerContract('USD')
  toggleCurrency('#amount-staked-per-contract', 'usd', 'nxm')
})

$('#amount-staked-per-contract-nxm').click(() => {
  renderAmountStakedPerContract('NXM')
  toggleCurrency('#amount-staked-per-contract', 'nxm', 'usd')
})

$.get('percent_nxm_supply_staked', (response) => {
  Plotly.newPlot('percentNxmSupplyStaked', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})

const renderTotalStakingReward = (currency) => {
  if (totalStakingReward !== undefined) {
    Plotly.newPlot('totalStakingReward', [{
      x: getDateTimesInLocalTimezone(Object.keys(totalStakingReward[currency])),
      y: Object.values(totalStakingReward[currency]),
      fill: 'tozeroy',
      type: 'scatter'
    }])
  }
}

$.get('total_staking_reward', (response) => {
  totalStakingReward = response
  $('#total-staking-reward-usd').click()
})

$('#total-staking-reward-usd').click(() => {
  renderTotalStakingReward('USD')
  toggleCurrency('#total-staking-reward', 'usd', 'nxm')
})

$('#total-staking-reward-nxm').click(() => {
  renderTotalStakingReward('NXM')
  toggleCurrency('#total-staking-reward', 'nxm', 'usd')
})

const renderStakingRewardPerContract = (currency) => {
  if (stakingRewardPerContract !== undefined) {
    Plotly.newPlot('stakingRewardPerContract', [{
      x: Object.keys(stakingRewardPerContract[currency]),
      y: Object.values(stakingRewardPerContract[currency]),
      type: 'bar'
    }])
  }
}

$.get('staking_reward_per_contract', (response) => {
  stakingRewardPerContract = response
  $('#staking-reward-per-contract-usd').click()
})

$('#staking-reward-per-contract-usd').click(() => {
  renderStakingRewardPerContract('USD')
  toggleCurrency('#staking-reward-per-contract', 'usd', 'nxm')
})

$('#staking-reward-per-contract-nxm').click(() => {
  renderStakingRewardPerContract('NXM')
  toggleCurrency('#staking-reward-per-contract', 'nxm', 'usd')
})

const renderAllStakes = (currency) => {
  if (allStakes !== undefined) {
    table = $('#stakeDataTable').DataTable()
    table.clear()
    for (stake of allStakes) {
      stakedAmount = 0
      if (currency === 'USD') {
        stakedAmount = '$' + stake['amount_usd'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      } else {
        stakedAmount = stake['amount'].toLocaleString() + ' NXM'
      }

      table.row.add([
        stake['contract_name'],
        stake['address'],
        stakedAmount,
        toLocalTimezone(stake['start_time']),
        toLocalTimezone(stake['end_time'])
      ])
    }
    table.draw()
  }
}

$.get('all_stakes', (response) => {
  allStakes = response
  $('#all-stakes-usd').click()
})

$('#all-stakes-usd').click(() => {
  renderAllStakes('USD')
  toggleCurrency('#all-stakes', 'usd', 'nxm')
})

$('#all-stakes-nxm').click(() => {
  renderAllStakes('NXM')
  toggleCurrency('#all-stakes', 'nxm', 'usd')
})
