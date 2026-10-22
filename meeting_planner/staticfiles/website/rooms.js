text = document.getElementById("selectedroom");

document.querySelectorAll(".room").forEach((room) => {
    room.addEventListener("mouseover", (event) => {
        const id = event.currentTarget.id;
        text.textContent = `Current room is: ${id}`;
        
    });
});

document.querySelectorAll(".room").forEach((room) => {
    room.addEventListener("mouseenter", () => {
        text.style.display = "block";
        text.textContent = room.id;
    });

    room.addEventListener("mouseleave", () => {
        text.style.display = "none";
    });
});

document.addEventListener("mousemove", (event) => {
    text.style.left = `${event.clientX + 15}px`;
    text.style.top = `${event.clientY - 15}px`;
});