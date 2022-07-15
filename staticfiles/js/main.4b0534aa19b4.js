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

// Auto Search
var searchForm = $('.search-form')
var serchButton = $('.searchbuttonnF')
var searchInput = searchForm.find("[name='q']") // input name='q'
var typingTimer
var typingInterval = 3000 // 2 seconds
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
  serchButton.html("<i class='fa fa-spin fa-spinner' style='border-radius: 8px'></i> Searching...")
}

function perfomSearch() {
  displaySearching()
  var query = searchInput.val()
  setTimeout(function () {
    window.location.href = '/codes-examples/?q=' + query
  }, 1000)
}
// timeout 1 sec means take 1 sec to display search result
//Displaying Loading text on every page
$('body').append('<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>')
$(window).on('load', function () {
  setTimeout(removeLoader, 200) //wait for page load PLUS two seconds.
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





//password generator 
const resultEl = document.getElementById('result')
const lengthEl = document.getElementById('length')
const uppercaseEl = document.getElementById('uppercase')
const lowercaseEl = document.getElementById('lowercase')
const numbersEl = document.getElementById('numbers')
const symbolsEl = document.getElementById('symbols')
const generateEl = document.getElementById('generate')
const clipboardEl = document.getElementById('clipboard')

const randomFunc = {
  lower: getRandomLower,
  upper: getRandomUpper,
  number: getRandomNumber,
  symbol: getRandomSymbol,
}

clipboardEl.addEventListener('click', () => {
  const textarea = document.createElement('textarea')
  const password = resultEl.innerText

  if (!password) {
    return
  }

  textarea.value = password
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand('copy')
  textarea.remove()
  alert('Password copied to clipboard!')
})

generateEl.addEventListener('click', () => {
  const length = +lengthEl.value
  const hasLower = lowercaseEl.checked
  const hasUpper = uppercaseEl.checked
  const hasNumber = numbersEl.checked
  const hasSymbol = symbolsEl.checked

  resultEl.innerText = generatePassword(hasLower, hasUpper, hasNumber, hasSymbol, length)
})

function generatePassword(lower, upper, number, symbol, length) {
  let generatedPassword = ''
  const typesCount = lower + upper + number + symbol
  const typesArr = [{ lower }, { upper }, { number }, { symbol }].filter((item) => Object.values(item)[0])

  if (typesCount === 0) {
    return ''
  }

  for (let i = 0; i < length; i += typesCount) {
    typesArr.forEach((type) => {
      const funcName = Object.keys(type)[0]
      generatedPassword += randomFunc[funcName]()
    })
  }

  const finalPassword = generatedPassword.slice(0, length)

  return finalPassword
}

function getRandomLower() {
  return String.fromCharCode(Math.floor(Math.random() * 26) + 97)
}

function getRandomUpper() {
  return String.fromCharCode(Math.floor(Math.random() * 26) + 65)
}

function getRandomNumber() {
  return String.fromCharCode(Math.floor(Math.random() * 10) + 48)
}

function getRandomSymbol() {
  const symbols = '!@#$%^&*(){}[]=<>/,.'
  return symbols[Math.floor(Math.random() * symbols.length)]
}