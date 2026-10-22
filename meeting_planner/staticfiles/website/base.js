const button = document.getElementById("darklight");

button.addEventListener("change", function () {
  document.body.classList.toggle("dark-mode", button.checked);
});