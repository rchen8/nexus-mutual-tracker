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

  // Scroll to top button appear
  $(document).on('scroll', () => {
    const scrollDistance = $(this).scrollTop()
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn()
    } else {
      $('.scroll-to-top').fadeOut()
    }
  })

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', (event) => {
    const $anchor = $(this)
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo')
    event.preventDefault()
  })
})(jQuery)

const toLocalTimezone = (date) => {
  date = new Date(Date.parse(date))
  date.setMinutes(date.getMinutes() - new Date().getTimezoneOffset())
  let date_string = date.getFullYear() + '-'
  date_string += (date.getMonth() + 1) <= 9 ? '0' + (date.getMonth() - 1) + '-' :
      (date.getMonth() - 1) + '-'
  date_string += date.getDate() <= 9 ? '0' + date.getDate() + ' ' : date.getDate() + ' '
  date_string += date.toLocaleTimeString('en-US', {'hour12' : false})
  return date_string
}

const getDateTimesInLocalTimezone = (dates) => {
  for (let i = 0; i < dates.length; i++) {
    dates[i] = toLocalTimezone(dates[i])
  }
  return dates
}
