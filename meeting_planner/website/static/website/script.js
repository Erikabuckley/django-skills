date = new Date().toLocaleDateString()
document.getElementById("date").textContent = date


navigator.geolocation.getCurrentPosition(showPosition, showError);

async function showPosition(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  const API_KEY = 'abbe1799e6459da348fad1d745160b1a';

  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;

  try {
    const weather = await getWeather(url);

    document.getElementById("location").textContent =
      `Location: ${weather.name}`;
      
      document.getElementById("temp").textContent =
      `Temperature: ${weather.main.temp}°C`;

      document.getElementById("weather").textContent =
      `Conditions: ${weather.weather[0].description}`;
  } catch (error) {
    document.getElementById("weather").textContent =
      `Error fetching weather: ${error.message}`;
  }
}

function showError(error) {
  document.getElementById("weather").textContent =
    `Unable to retrieve location: ${error.message}`;
}

async function getWeather(url) {
  const response = await fetch(url);

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      `Weather API request failed (${response.status}): ${message}`
    );
  }

  return response.json();
}