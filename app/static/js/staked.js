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
  renderTotalStakingReward('USD')
})

$('#total-staking-reward-usd').click(() => {
  renderTotalStakingReward('USD')
})

$('#total-staking-reward-nxm').click(() => {
  renderTotalStakingReward('NXM')
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
  renderStakingRewardPerContract('USD')
})

$('#staking-reward-per-contract-usd').click(() => {
  renderStakingRewardPerContract('USD')
})

$('#staking-reward-per-contract-nxm').click(() => {
  renderStakingRewardPerContract('NXM')
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
  renderAllStakes('USD')
})

$('#all-stakes-usd').click(() => {
  renderAllStakes('USD')
})

$('#all-stakes-nxm').click(() => {
  renderAllStakes('NXM')
})
