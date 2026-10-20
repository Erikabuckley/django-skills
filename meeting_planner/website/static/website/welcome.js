const canvas = document.getElementById("canvas");
console.log("Canvas:", canvas);
console.log('hello')
const ctx = canvas.getContext("2d");
let radius = canvas.height / 2;
ctx.translate(radius, radius);
radius = radius * 0.90
drawClock();
setInterval(drawClock, 1000);


function drawClock() {
  drawFace(ctx, radius);
  drawNumbers(ctx, radius);
  drawTime(ctx, radius);
}

function drawFace(ctx, radius) {
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, 2*Math.PI);
  ctx.fillStyle = 'white';
  ctx.fill();
  ctx.strokeStyle = 'grey';
  ctx.lineWidth = radius*0.05;
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(0, 0, radius*0.05, 0, 2*Math.PI);
  ctx.fillStyle = 'grey';
  ctx.fill();
}

function drawNumbers(ctx, radius) {
  ctx.font = radius*0.15 + "px arial";
  ctx.textBaseline="middle";
  ctx.textAlign="center";
  for(let num = 1; num < 13; num++){
    let ang = num * Math.PI / 6;
    ctx.rotate(ang);
    ctx.translate(0, -radius*0.85);
    ctx.rotate(-ang);
    ctx.fillText(num.toString(), 0, 0);
    ctx.rotate(ang);
    ctx.translate(0, radius*0.85);
    ctx.rotate(-ang);
  }
}

function drawTime(ctx, radius){
    const now = new Date();
    let hour = now.getHours();
    let minute = now.getMinutes();
    let second = now.getSeconds();
    //hour
    hour=hour%12;
    hour=(hour*Math.PI/6)+
    (minute*Math.PI/(6*60))+
    (second*Math.PI/(360*60));
    drawHand(ctx, hour, radius*0.5, radius*0.04);
    //minute
    minute=(minute*Math.PI/30)+(second*Math.PI/(30*60));
    drawHand(ctx, minute, radius*0.65, radius*0.04);
    // second
    second=(second*Math.PI/30);
    drawHand(ctx, second, radius*0.7, radius*0.02);
}

function drawHand(ctx, pos, length, width) {
    ctx.beginPath();
    ctx.lineWidth = width;
    ctx.lineCap = "round";
    ctx.moveTo(0,0);
    ctx.rotate(pos);
    ctx.lineTo(0, -length);
    ctx.stroke();
    ctx.rotate(-pos);
}

date = new Date().toLocaleDateString()
document.getElementById("date").textContent = date


navigator.geolocation.getCurrentPosition(showPosition, showError, {enableHighAccuracy: false,});

async function showPosition(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;

  try {


    const weather = await getWeather(lat, lon);

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

async function getWeather(lat, lon) {
    const response = await fetch(
        `/api/meeting-data/?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}`
    );

    if (!response.ok) {
        throw new Error("Failed to load meeting data");
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