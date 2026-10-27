# Smart Care — Hospital Management System

A desktop mini-project built with Python, Tkinter, and SQLite.

## Features
- Patient registration and patient listing
- Doctor registration and doctor listing
- Appointment scheduling and completion status
- Billing and paid/unpaid status
- Local SQLite database created automatically

## Requirements
- Python 3.10+ recommended
- Tkinter (usually included with Python on Windows)
- No pip packages required

## Run on Windows
1. Extract `smart_care_hospital_management.zip`.
2. Open the `smart_care_hospital_management` folder in VS Code.
3. Open the terminal in that folder.
4. Run:
   ```powershell
   python main.py
   ```
5. The application title will show **Smart Care - Hospital Management System**.
6. The database `smart_care_hospital.db` will be created automatically.

## Database tables
- `patients`
- `doctors`
- `appointments`
- `bills`

## Demo steps
1. Add a doctor, such as “Dr. Rao” in “Cardiology”.
2. Add a fictional patient.
3. Schedule an appointment using `YYYY-MM-DD HH:MM`.
4. Create a bill and mark it as paid.

## Important
This is an educational project, not a production clinical system. Use fictional data only. Real deployments need authentication, role-based permissions, audit logs, secure backups, privacy controls, and stronger validation.
