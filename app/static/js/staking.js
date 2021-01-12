let totalAmountStaked = undefined
let amountStakedPerProject = undefined
let topStakers = undefined
let totalStakingReward = undefined
let stakingRewardPerProject = undefined

const endpoints = [
  'total_amount_staked',
  'amount_staked_per_project',
  'top_stakers',
  'total_staking_reward',
  'staking_reward_per_project'
]

Promise.all(endpoints.map(getData)).then(data => {
  totalAmountStaked = data[0]
  amountStakedPerProject = data[1]
  topStakers = data[2]
  totalStakingReward = data[3]
  stakingRewardPerProject = data[4]

  renderStats()
  setTimeout(() => {renderGraphs()}, 0)
})

const renderStats = () => {
  $('#currentTotalAmountStaked').text(getCurrentValue(totalAmountStaked, ['USD', 'NXM']))
  $('#currentTotalStakingReward').text(getCurrentValue(totalStakingReward, ['USD', 'NXM']))
}

const renderGraphs = () => {
  $('#total-amount-staked-usd').click()
  $('#amount-staked-per-project-usd').click()
  $('#top-stakers-usd').click()
  $('#total-staking-reward-usd').click()
  $('#staking-reward-per-project-usd').click()
}

const renderTotalAmountStaked = (currency) => {
  Plotly.newPlot('totalAmountStaked', [{
    x: Object.keys(totalAmountStaked[currency]),
    y: Object.values(totalAmountStaked[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#total-amount-staked-usd').click(() => {
  renderTotalAmountStaked('USD')
  toggleCurrency('#total-amount-staked', 'usd', 'nxm')
})

$('#total-amount-staked-nxm').click(() => {
  renderTotalAmountStaked('NXM')
  toggleCurrency('#total-amount-staked', 'nxm', 'usd')
})

const renderAmountStakedPerProject = (currency) => {
  Plotly.newPlot('amountStakedPerProject', [{
    x: Object.keys(amountStakedPerProject[currency]),
    y: Object.values(amountStakedPerProject[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#amount-staked-per-project-usd').click(() => {
  renderAmountStakedPerProject('USD')
  toggleCurrency('#amount-staked-per-project', 'usd', 'nxm')
})

$('#amount-staked-per-project-nxm').click(() => {
  renderAmountStakedPerProject('NXM')
  toggleCurrency('#amount-staked-per-project', 'nxm', 'usd')
})

const renderTopStakers = (currency) => {
  Plotly.newPlot('topStakers', [{
    labels: Object.keys(topStakers[currency]),
    values: Object.values(topStakers[currency]),
    type: 'pie',
    textinfo: 'none'
  }], {}, {responsive: true})
}

$('#top-stakers-usd').click(() => {
  renderTopStakers('USD')
  toggleCurrency('#top-stakers', 'usd', 'nxm')
})

$('#top-stakers-nxm').click(() => {
  renderTopStakers('NXM')
  toggleCurrency('#top-stakers', 'nxm', 'usd')
})

const renderTotalStakingReward = (currency) => {
  Plotly.newPlot('totalStakingReward', [{
    x: Object.keys(totalStakingReward[currency]),
    y: Object.values(totalStakingReward[currency]),
    fill: 'tozeroy',
    type: 'scattergl'
  }], {}, {responsive: true})
}

$('#total-staking-reward-usd').click(() => {
  renderTotalStakingReward('USD')
  toggleCurrency('#total-staking-reward', 'usd', 'nxm')
})

$('#total-staking-reward-nxm').click(() => {
  renderTotalStakingReward('NXM')
  toggleCurrency('#total-staking-reward', 'nxm', 'usd')
})

const renderStakingRewardPerProject = (currency) => {
  Plotly.newPlot('stakingRewardPerProject', [{
    x: Object.keys(stakingRewardPerProject[currency]),
    y: Object.values(stakingRewardPerProject[currency]),
    type: 'bar'
  }], {}, {responsive: true})
}

$('#staking-reward-per-project-usd').click(() => {
  renderStakingRewardPerProject('USD')
  toggleCurrency('#staking-reward-per-project', 'usd', 'nxm')
})

$('#staking-reward-per-project-nxm').click(() => {
  renderStakingRewardPerProject('NXM')
  toggleCurrency('#staking-reward-per-project', 'nxm', 'usd')
})
