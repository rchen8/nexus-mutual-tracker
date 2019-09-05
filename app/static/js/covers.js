$.get('active_cover_amount', (response) => {
  Plotly.newPlot('activeCoverAmount', [{
    x: getDateTimesInLocalTimezone(Object.keys(response)),
    y: Object.values(response),
    fill: 'tozeroy',
    type: 'scatter'
  }])
})

$.get('active_cover_amount_per_contract', (response) => {
  Plotly.newPlot('activeCoverAmountPerContract', [{
    x: Object.keys(response),
    y: Object.values(response),
    type: 'bar'
  }])
})

$.get('all_covers', (response) => {
  let table = document.getElementById('covers')
  for (cover of response) {
    let row = ''
    row += '<tr>'
    row += '<td>' + cover['cover_id'] + '</td>'
    row += '<td>' + cover['contract_name'] + '</td>'
    row += '<td>' + cover['amount'].toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '</td>'
    row += '<td>' + toLocalTimezone(cover['start_time']) + '</td>'
    row += '<td>' + toLocalTimezone(cover['end_time']) + '</td>'
    row += '</tr>'
    table.innerHTML += row
  }
  $('#dataTable').DataTable();
})
