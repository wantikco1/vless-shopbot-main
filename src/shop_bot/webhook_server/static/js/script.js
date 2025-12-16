document.addEventListener('DOMContentLoaded', function () {
	function initializePasswordToggles() {
		const togglePasswordButtons = document.querySelectorAll('.toggle-password')
		togglePasswordButtons.forEach(button => {
			button.addEventListener('click', function () {
				const parent =
					this.closest('.form-group') || this.closest('.password-wrapper')
				if (!parent) return

				const passwordInput = parent.querySelector('input')
				if (!passwordInput) return

				if (passwordInput.type === 'password') {
					passwordInput.type = 'text'
					this.textContent = '🙈'
				} else {
					passwordInput.type = 'password'
					this.textContent = '👁️'
				}
			})
		})
	}

	function setupBotControlForms() {
		const controlForms = document.querySelectorAll(
			'form[action*="start-bot"], form[action*="stop-bot"]'
		)

		controlForms.forEach(form => {
			form.addEventListener('submit', function () {
				const button = form.querySelector('button[type="submit"]')
				if (button) {
					button.disabled = true
					if (form.action.includes('start')) {
						button.textContent = 'Запускаем...'
					} else if (form.action.includes('stop')) {
						button.textContent = 'Останавливаем...'
					}
				}
				setTimeout(function () {
					window.location.reload()
				}, 1000) // 1 second
			})
		})
	}

	function setupConfirmationForms() {
		const confirmationForms = document.querySelectorAll('form[data-confirm]')
		confirmationForms.forEach(form => {
			form.addEventListener('submit', function (event) {
				const message = form.getAttribute('data-confirm')
				if (!confirm(message)) {
					event.preventDefault()
				}
			})
		})
	}

	function initializeDashboardCharts() {
		const usersChartCanvas = document.getElementById('newUsersChart')
		if (!usersChartCanvas || typeof CHART_DATA === 'undefined') {
			return
		}

		function prepareChartData(data, label, color) {
			const labels = []
			const values = []
			const today = new Date()

			for (let i = 29; i >= 0; i--) {
				const date = new Date(today)
				date.setDate(today.getDate() - i)
				const dateString = date.toISOString().split('T')[0]
				const formattedDate = `${date.getDate().toString().padStart(2, '0')}.${(
					date.getMonth() + 1
				)
					.toString()
					.padStart(2, '0')}`
				labels.push(formattedDate)
				values.push(data[dateString] || 0)
			}

			return {
				labels: labels,
				datasets: [
					{
						label: label,
						data: values,
						borderColor: color,
						backgroundColor: color + '33',
						borderWidth: 2,
						fill: true,
						tension: 0.3,
					},
				],
			}
		}

		function updateChartFontsAndLabels(chart) {
			const isMobile = window.innerWidth <= 768
			const isVerySmall = window.innerWidth <= 470
			chart.options.scales.x.ticks.font.size = isMobile ? 10 : 12
			chart.options.scales.y.ticks.font.size = isMobile ? 10 : 12
			chart.options.plugins.legend.labels.font.size = isMobile ? 12 : 14
			chart.options.scales.x.ticks.maxTicksLimit = isMobile ? 8 : 15
			chart.options.scales.x.ticks.display = !isVerySmall
			chart.options.scales.y.ticks.display = !isVerySmall
			chart.options.plugins.legend.display = !isVerySmall
			chart.update()
		}

		const usersCtx = usersChartCanvas.getContext('2d')
		const usersChartData = prepareChartData(
			CHART_DATA.users,
			'Новых пользователей в день',
			'#007bff'
		)
		const usersChart = new Chart(usersCtx, {
			type: 'line',
			data: usersChartData,
			options: {
				scales: {
					y: {
						beginAtZero: true,
						ticks: {
							precision: 0,
							font: {
								size: window.innerWidth <= 768 ? 10 : 12,
							},
							display: window.innerWidth > 470,
						},
					},
					x: {
						ticks: {
							font: {
								size: window.innerWidth <= 768 ? 10 : 12,
							},
							maxTicksLimit: window.innerWidth <= 768 ? 8 : 15,
							maxRotation: 45,
							minRotation: 45,
							display: window.innerWidth > 470,
						},
					},
				},
				responsive: true,
				maintainAspectRatio: false,
				layout: {
					autoPadding: true,
					padding: 0,
				},
				plugins: {
					legend: {
						labels: {
							font: {
								size: window.innerWidth <= 768 ? 12 : 14,
							},
							display: window.innerWidth > 470,
						},
					},
				},
			},
		})

		const keysChartCanvas = document.getElementById('newKeysChart')
		if (!keysChartCanvas) return

		const keysCtx = keysChartCanvas.getContext('2d')
		const keysChartData = prepareChartData(
			CHART_DATA.keys,
			'Новых ключей в день',
			'#28a745'
		)
		const keysChart = new Chart(keysCtx, {
			type: 'line',
			data: keysChartData,
			options: {
				scales: {
					y: {
						beginAtZero: true,
						ticks: {
							precision: 0,
							font: {
								size: window.innerWidth <= 768 ? 10 : 12,
							},
							display: window.innerWidth > 470,
						},
					},
					x: {
						ticks: {
							font: {
								size: window.innerWidth <= 768 ? 10 : 12,
							},
							maxTicksLimit: window.innerWidth <= 768 ? 8 : 15,
							maxRotation: 45,
							minRotation: 45,
							display: window.innerWidth > 470,
						},
					},
				},
				responsive: true,
				maintainAspectRatio: false,
				layout: {
					autoPadding: true,
					padding: 0,
				},
				plugins: {
					legend: {
						labels: {
							font: {
								size: window.innerWidth <= 768 ? 12 : 14,
							},
							display: window.innerWidth > 470,
						},
					},
				},
			},
		})

		window.addEventListener('resize', () => {
			updateChartFontsAndLabels(usersChart)
			updateChartFontsAndLabels(keysChart)
		})
	}

	initializePasswordToggles()
	setupBotControlForms()
	setupConfirmationForms()
	initializeDashboardCharts()
	setupReferralModal()
})

// Переменная для хранения текущего user_id
let currentReferralUserId = null

function setupReferralModal() {
	// Закрытие модального окна при клике вне его
	const modal = document.getElementById('referralModal')
	if (modal) {
		window.onclick = function (event) {
			if (event.target === modal) {
				closeReferralModal()
			}
		}
	}
}

function openReferralModal(userId) {
	currentReferralUserId = userId
	const modal = document.getElementById('referralModal')
	if (modal) {
		modal.style.display = 'block'
		loadReferralData(userId)
	}
}

function closeReferralModal() {
	const modal = document.getElementById('referralModal')
	if (modal) {
		modal.style.display = 'none'
		currentReferralUserId = null
		document.getElementById('newBalance').value = ''
	}
}

function loadReferralData(userId) {
	const balanceElement = document.getElementById('referralBalance')
	const referralsList = document.getElementById('referralsList')
	
	balanceElement.textContent = 'Загрузка...'
	referralsList.innerHTML = '<p>Загрузка...</p>'
	
	fetch(`/users/referrals/${userId}`)
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				balanceElement.textContent = `${data.balance.toFixed(2)} RUB`
				
				if (data.referrals && data.referrals.length > 0) {
					let html = '<ul class="referrals-list-items">'
					data.referrals.forEach(ref => {
						const username = ref.username ? `@${ref.username}` : 'N/A'
						html += `<li>ID: ${ref.telegram_id} | ${username}</li>`
					})
					html += '</ul>'
					referralsList.innerHTML = html
				} else {
					referralsList.innerHTML = '<p>У пользователя пока нет рефералов.</p>'
				}
			} else {
				alert('Ошибка загрузки данных: ' + (data.error || 'Неизвестная ошибка'))
			}
		})
		.catch(error => {
			console.error('Error loading referral data:', error)
			alert('Ошибка загрузки данных о рефералах')
		})
}

function resetReferralBalance() {
	if (!currentReferralUserId) return
	
	if (!confirm('Вы уверены, что хотите обнулить реферальный баланс этого пользователя?')) {
		return
	}
	
	fetch(`/users/referrals/${currentReferralUserId}/reset`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		}
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				loadReferralData(currentReferralUserId)
				alert('Баланс успешно обнулен')
				// Обновляем страницу, чтобы обновить кнопку рефералки
				setTimeout(() => {
					window.location.reload()
				}, 500)
			} else {
				alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'))
			}
		})
		.catch(error => {
			console.error('Error resetting balance:', error)
			alert('Ошибка при обнулении баланса')
		})
}

function setReferralBalance() {
	if (!currentReferralUserId) return
	
	const balanceInput = document.getElementById('newBalance')
	const newBalance = parseFloat(balanceInput.value)
	
	if (isNaN(newBalance) || newBalance < 0) {
		alert('Введите корректное значение баланса (число >= 0)')
		return
	}
	
	if (!confirm(`Установить баланс ${newBalance.toFixed(2)} RUB для этого пользователя?`)) {
		return
	}
	
	fetch(`/users/referrals/${currentReferralUserId}/set`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ balance: newBalance })
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				balanceInput.value = ''
				loadReferralData(currentReferralUserId)
				alert('Баланс успешно установлен')
			} else {
				alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'))
			}
		})
		.catch(error => {
			console.error('Error setting balance:', error)
			alert('Ошибка при установке баланса')
		})
}
