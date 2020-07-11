let totalAmountStaked = undefined
let amountStakedPerContract = undefined
let topStakers = undefined
let totalStakingReward = undefined
let stakingRewardPerContract = undefined
let allStakes = undefined

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

const renderTopStakers = (currency) => {
  if (topStakers !== undefined) {
    Plotly.newPlot('topStakers', [{
      labels: Object.keys(topStakers[currency]),
      values: Object.values(topStakers[currency]),
      type: 'pie',
      textinfo: 'none'
    }])
  }
}

$.get('top_stakers', (response) => {
  topStakers = response
  $('#top-stakers-usd').click()
})

$('#top-stakers-usd').click(() => {
  renderTopStakers('USD')
  toggleCurrency('#top-stakers', 'usd', 'nxm')
})

$('#top-stakers-nxm').click(() => {
  renderTopStakers('NXM')
  toggleCurrency('#top-stakers', 'nxm', 'usd')
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
    const table = $('#stakeDataTable').DataTable()
    table.clear()
    for (let stake of allStakes) {
      let totalReward = 0
      let totalStaked = 0
      if (currency === 'USD') {
        totalReward = '$' + stake['total_reward_usd'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
        totalStaked = '$' + stake['total_staked_usd'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      } else {
        totalReward = stake['total_reward'].toLocaleString() + ' NXM'
        totalStaked = stake['total_staked'].toLocaleString() + ' NXM'
      }

      table.row.add([
        stake['contract_name'],
        stake['address'],
        totalReward,
        totalStaked,
        stake['estimated_yield'].toFixed(2) + '%'
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
