# Meeting Planner

A web-based meeting planning application built with Django. The application provides a central dashboard where users can view upcoming meetings, manage room bookings, browse a floor plan, and access useful daily information.

## Features

- **Dashboard:** A central overview of meetings and useful information.
- **Next Meeting:** Displays the user's next scheduled meeting, including its time, date, and room.
- **Your Meetings:** Lists upcoming meetings and provides an option to book a new meeting.
- **Meeting Management:** Create, edit, and manage meeting bookings.
- **Room Booking:** Assign meetings to rooms and check for scheduling conflicts to prevent overlapping bookings.
- **Rooms List:** View a floor plan to help users identify meeting rooms.
- **Past Meetings:** View previously scheduled meetings.
- **Weather Information:** Displays current weather conditions and temperature for a selected location.
- **Clock:** Displays an analogue clock on the dashboard.
- **Riddle of the Day:** Provides a daily riddle for users to solve.
- **Authentication:** Supports user login and access to authenticated features.

## Getting Started

### Prerequisites

To run the project locally, you will need:

- Python 3
- pip
- Git (optional)
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd meeting_planner
   ```

2. Create and activate a virtual environment:

   **Windows:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Static Files

The application uses Django's static-file system to manage CSS, JavaScript, and image assets.

During development, Django can serve static files when `DEBUG = True`.

For production or when running with `DEBUG = False`, configure `STATIC_ROOT` and `STATIC_URL` in `settings.py`, then run:

```bash
python manage.py collectstatic
```

If using WhiteNoise, ensure its middleware is configured to serve the collected static files.

## Running with Docker

To build and start the application using Docker Compose:

```bash
docker compose up --build
```

If using Docker directly, build the image with:

```bash
docker build -t meeting-planner .
```

```
docker run --env-file .env -p 8000:8000 meeting-planner
```
The Docker configuration should install the dependencies, copy the project files, collect static files, and start the application.
