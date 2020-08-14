(($) => {
  "use strict"

  // Toggle the side navigation
  $("#sidebarToggle").on('click', (e) => {
    e.preventDefault()
    $("body").toggleClass("sidebar-toggled")
    $(".sidebar").toggleClass("toggled")
  })

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', (e) => {
    if ($(window).width() > 768) {
      const e0 = e.originalEvent
      const delta = e0.wheelDelta || -e0.detail
      this.scrollTop += (delta < 0 ? 1 : -1) * 30
      e.preventDefault()
    }
  })
})(jQuery)

const getData = url => new Promise(response => $.get(url, response))

const getCurrentValue = (object, currencies, price) => {
  if (currencies === null) {
    return object[Object.keys(object)[Object.keys(object).length - 1]]
  } else {
    text = ''
    for (currency of currencies) {
      value = object[currency]
          [Object.keys(object[currency])[Object.keys(object[currency]).length - 1]]
      if (text !== '') {
        text += ' / '
      }
      if (currency === 'USD') {
        text += price ? '$' + value.toFixed(2) : '$' + Math.round(value).toLocaleString()
      } else if (currency === 'ETH') {
        text += price ? value.toFixed(4) + ' ETH' : Math.round(value).toLocaleString() + ' ETH'
      } else if (currency === 'NXM') {
        text += Math.round(value).toLocaleString() + ' NXM'
      }
    }
    return text
  }
}

const toggleCurrency = (query_selector, activeCurrency, inactiveCurrency) => {
  $(query_selector + '-' + activeCurrency).attr('disabled', 'disabled')
  $(query_selector + '-' + activeCurrency).css({'color': 'black', 'background-color': 'white'})
  $(query_selector + '-' + inactiveCurrency).removeAttr('disabled')
  $(query_selector + '-' + inactiveCurrency).css('background-color', 'grey')
}
