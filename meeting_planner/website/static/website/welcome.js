date = new Date().toLocaleDateString()
document.getElementById("date").textContent = date


navigator.geolocation.getCurrentPosition(showPosition, showError), {enableHighAccuracy: false,};

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
      `${weather.main.temp}°C`;

      document.getElementById("weather").textContent =
      `Conditions: ${weather.weather[0].description}`;

      p = calc_temp(weather.main.temp);
      document.getElementById("success-value").setAttribute("stroke-dasharray", `${p}% ${100 - p}%`);      
      t = getTempColour(p);
      document.getElementById("success-value").setAttribute("stroke", t);

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


function calc_temp(temp){
  if (temp < 0){
    return 15
  }else if (temp > 45){
    return 70
  }
  else{
    return 15 + (temp/40) * 50
  }

}

function getTempColour(temp) {
    // Clamp temperature between 15 and 70
    const minTemp = 15;
    const maxTemp = 70;

    const t = Math.max(0, Math.min(1, (temp - minTemp) / (maxTemp - minTemp)));

    const colours = [
        { stop: 0,    r: 0,   g: 0,   b: 255 },
        { stop: 1 / 3, r: 0,   g: 255, b: 0 },
        { stop: 2 / 3, r: 255, g: 165, b: 0 },
        { stop: 1,    r: 255, g: 0,   b: 0 }
    ];

    // Find the two colours to blend between
    let i = 0;

    while (i < colours.length - 2 && t > colours[i + 1].stop) {
        i++;
    }

    const start = colours[i];
    const end = colours[i + 1];

    // Calculate position between the two colour stops
    const localT = (t - start.stop) / (end.stop - start.stop);

    const r = Math.round(start.r + (end.r - start.r) * localT);
    const g = Math.round(start.g + (end.g - start.g) * localT);
    const b = Math.round(start.b + (end.b - start.b) * localT);

    return `rgb(${r}, ${g}, ${b})`;
}


text = document.getElementById("selectedroom");

document.querySelectorAll(".room").forEach((room) => {
    room.addEventListener("mouseover", (event) => {
        const id = event.currentTarget.id;
        console.log
        text.textContent = `Current room is" ${id}`;
        
    });
});