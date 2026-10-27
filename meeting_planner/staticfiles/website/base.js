// toggle to turn dark mode on or off
const button = document.getElementById("darklight");

button.addEventListener("change", function () {
  document.body.classList.toggle("dark-mode", button.checked);
});