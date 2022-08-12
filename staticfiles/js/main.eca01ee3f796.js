// message alert fade out
setTimeout(function () {
  $('#alert').fadeOut('fast')
}, 5000)

//Display time date
function showTime() {
  var date = new Date()
  var h = date.getHours() // 0 - 23
  var m = date.getMinutes() // 0 - 59
  var s = date.getSeconds() // 0 - 59
  var session = 'AM'

  var d = date.getDate()
  var mn = date.getMonth()
  var y = date.getFullYear()
  var dS = d + '-' + (mn + 1) + '-' + y

  if (h == 0) {
    h = 12
  }

  if (h > 12) {
    h = h - 12
    session = 'PM'
  }

  h = h < 10 ? '0' + h : h
  m = m < 10 ? '0' + m : m
  s = s < 10 ? '0' + s : s

  var time = h + ':' + m + ':' + s + ' ' + session + ' ' + ' ' + ' ' + '|  ' + dS
  document.getElementById('MyClockDisplay').innerText = time
  document.getElementById('MyClockDisplay').textContent = time

  setTimeout(showTime, 1000)
}

showTime()

// for main notes page Auto Search will trigger if user not press enter
var searchForm = $('.search-form')
var serchButton = $('.searchbuttonnF')
var searchInput = searchForm.find("[name='q']") // input name='q'
var typingTimer
var typingInterval = 2000 // 2 seconds
var searchBtn = searchForm.find("[type='submit']")
searchInput.keyup(function (event) {
  // key released
  clearTimeout(typingTimer)

  typingTimer = setTimeout(perfomSearch, typingInterval)
})

searchInput.keydown(function (event) {
  // key pressed
  clearTimeout(typingTimer)
})

function displaySearching() {
  serchButton.addClass('disabled')
  serchButton.html("<i class='fa fa-spin fa-spinner text-light' style='border-radius: 8px;color:white;'></i> Searching...")
}

function perfomSearch() {
  displaySearching()
  var query = searchInput.val()
  setTimeout(function () {
    window.location.href = '/codes-lists/?q=' + query
  }, 1000)
}
// timeout 1 sec means take 1 sec to display search result

// for fav page Auto Search will trigger if user not press enter
var searchForm1 = $('.search-form1')
var serchButton1 = $('.searchbuttonnF1')
var searchInput1 = searchForm1.find("[name='q1']") // input name='q1'
var typingTimer1
var typingInterval = 2000 // 2 seconds
var searchBtn1 = searchForm1.find("[type='submit']")
searchInput1.keyup(function (event) {
  // key released
  clearTimeout(typingTimer)

  typingTimer1 = setTimeout(perfomSearch, typingInterval)
})

searchInput1.keydown(function (event) {
  // key pressed
  clearTimeout(typingTimer1)
})

function displaySearching() {
  serchButton1.addClass('disabled')
  serchButton1.html("<i class='fa fa-spin fa-spinner text-light' style='border-radius: 8px;color:white;'></i> Searching1...")
}

function perfomSearch() {
  displaySearching()
  var query = searchInput1.val()
  setTimeout(function () {
    window.location.href = '/favourites-codes-lists/?q=' + query
  }, 1000)
}
// timeout 1 sec means take 1 sec to display search result

//Displaying Loading text on every page
$('body').append('<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>')
$(window).on('load', function () {
  setTimeout(removeLoader, 150) //wait for page load PLUS two seconds.
})
function removeLoader() {
  $('#loadingDiv').fadeOut(500, function () {
    // fadeOut complete. Remove the loading div
    $('#loadingDiv').remove() //makes page more lightweight
  })
}

// bootstrap spinner on every page load

var preloader = document.getElementById('loading')

function myLoading() {
  preloader.style.display = 'none'
}
