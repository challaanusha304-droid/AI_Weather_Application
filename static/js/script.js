const cityInput = document.querySelector('#city');
const status = document.querySelector('#status');
const card = document.querySelector('#weather-card');
const assistant = document.querySelector('#assistant');
const answer = document.querySelector('#answer');
let currentCity = '';

document.querySelector('#weather-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  currentCity = cityInput.value.trim();
  status.textContent = 'Loading weather…'; card.classList.add('hidden'); assistant.classList.add('hidden');
  try {
    const response = await fetch(`/api/weather?city=${encodeURIComponent(currentCity)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    card.innerHTML = `<h2>${data.city}, ${data.country}</h2><p>${data.description}</p><div class="temp">${data.temperature}°C</div><div class="metrics"><span>Feels ${data.feels_like}°C</span><span>${data.humidity}% humidity</span><span>${data.wind_speed} m/s wind</span></div>`;
    card.classList.remove('hidden'); assistant.classList.remove('hidden'); status.textContent = '';
  } catch (error) { status.textContent = error.message || 'Unable to load weather.'; }
});

document.querySelector('#question-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const question = document.querySelector('#question').value.trim(); answer.textContent = 'Thinking…';
  try {
    const response = await fetch('/api/ask', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ city: currentCity, question }) });
    const data = await response.json(); if (!response.ok) throw new Error(data.error); answer.textContent = data.answer;
  } catch (error) { answer.textContent = error.message || 'Unable to answer right now.'; }
});
