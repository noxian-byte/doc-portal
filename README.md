# doc-portal
doctor's office scheduler.

A simple Flask-based API that has 3 user portals:

## API Endpoints

### Main Routes:
- **`/`** - Displays the main menu (can later be used for UI if needed).
- **`/receptionist_portal`** - Redirects to the receptionist portal.
- **`/doctor_portal`** - Redirects to the doctor portal.
- **`/patient_portal`** - Redirects to the patient portal.
- **`/exit`** - Ends the session and displays an exit message.

### Receptionist Portal (`/receptionist_portal`):
- Access to the receptionist's dashboard and appointment management.

### Doctor Portal (`/doctor_portal`):
- Access to the doctor's dashboard to view scheduled appointments and patient information.

### Patient Portal (`/patient_portal`):
- Allows patients to book, view, and cancel appointments.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd doc-portal 

2. Create a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate` 
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```



