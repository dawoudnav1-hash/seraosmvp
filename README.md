# SeraOS 🌌

**SeraOS** is a "Super Agentic" platform for students, designed to organize your academic life with a premium, glassmorphic UI and a powerful AI assistant named **Octavia**.

## Features

-   **Octavia Agent**: A "Know-It-All" AI that can answer questions (via Wikipedia), draft essay outlines, and manage your tasks. Supports **Voice Interaction**.
-   **Glassmorphism UI**: A stunning, modern dark-mode interface with smooth animations.
-   **Task Management**: specialized views for assignments, including "Break Down" and "Research" tools.
-   **Subject Dashboards**: Dedicated spaces for each of your courses.
-   **Integrations Hub**: Manage connections to Canvas, Outlook, and Drive.

## Tech Stack

-   **Backend**: Python (Flask)
-   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
-   **AI/Data**: `wikipedia` library, Web Speech API

## Setup & Run

1.  **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```

2.  **Start the Server**:
    ```bash
    python3 app.py
    ```

3.  **Open in Browser**:
    Go to [http://127.0.0.1:3000](http://127.0.0.1:3000)

## Project Structure

-   `app.py`: Main Flask application.
-   `octavia.py`: Logic for the AI agent.
-   `canvas_integration.py`: Mock service for LMS data.
-   `templates/`: HTML files for all pages.
-   `static/`: CSS and JavaScript files.

## License
Proprietary - Built for SeraOS.
