## How to Run the Project

To start the Simple Data Management application, follow these steps:

### 1. Open Your Terminal
Launch your terminal or command prompt.

### 2. Navigate to the Project Directory
Use the `cd` command to move into the project folder:
```bash
cd path/to/your/project/simple-data-management
```

### 3. Navigate to the Flask App Directory
Inside the project, move into the `flask_app` directory:
```bash
cd flask_app
```

### 4. Start the Backend API
The backend API must be running before the client-side app.

From the root of the project (e.g., `simple-data-management/`), run:
```bash
python -m server.api
```

This starts the backend API that handles all data processing and storage.

### 5. Start the Frontend (Flask Client)
Open a new terminal window. Inside the `flask_app` directory, run:
```bash
python app.py
```

This launches the front-end interface that communicates with the backend.

### 6. Access the Application
Once both services are running, open the local server URL printed in your terminal (e.g., `http://127.0.0.1:8000`) in your browser, or Ctrl + click it directly from your terminal.

---

## What the App Does

Simple Data Management is a full-stack web application that allows users to manage individual records using a clean and responsive interface.

### Core Features
- View Records – Browse all stored records via a card-based layout on `records.html`.
- Add Records – Use the form on `create.html` to input first name, last name, and date of birth with real-time validation.
- Update Records – Click the edit icon on a card to modify record details through a pre-filled modal.
- Delete Records – Use the delete (trash bin) icon to remove a specific record.

### Tech Stack
- Frontend: Flask, Jinja2, Bootstrap, JavaScript
- Backend API: Flask (RESTful endpoints)
- Data Storage: CSV file (`students.csv`)
