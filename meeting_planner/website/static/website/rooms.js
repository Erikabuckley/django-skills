// fills the box by the mouse with the room hovered over
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

// colours the room due to its availability
document.querySelectorAll(".room").forEach((room) => {
    color_floorplan(room)
});

async function color_floorplan(room) {
    try {
        const response = await getOccupied(room.id);

        occupied = response.occupied;
        if (occupied) {
            room.style.fill = 'rgba(255, 20, 20, 0.55)'
        }
        else {
            room.style.fill = 'rgba(55, 246, 109, 0.39)'
        }

    } catch (error) {
        document.getElementById("weather").textContent =
            `Error fetching weather: ${error.message}`;
    }
}


async function getOccupied(room_name) {
    const response = await fetch(
        `/api/meeting-occupied/?name=${encodeURIComponent(room_name)}`
    );

    if (!response.ok) {
        throw new Error("Failed to load occupied");
    }

    return response.json();
}

