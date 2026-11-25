# Student Feedback Analytics System

A Flask student feedback application with student registration, immutable feedback submissions, administrator management, and Chart.js analytics. It uses SQLite by default, so the client does not need to install or configure MySQL.

## Setup

1. Install Python 3.10+.
2. Create a virtual environment and install dependencies:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and keep the SQLite `DATABASE_URL`.
4. Create initial reference data and the admin account:

   ```powershell
   python seed.py
   ```

5. Start the server:

   ```powershell
   python app.py
   ```

Open `http://127.0.0.1:5000`. The default seed credentials are `admin@example.com` / `admin123`; change them in `.env` before deployment.

The SQLite database file `student_feedback.db` is created automatically. MySQL remains supported if a MySQL `DATABASE_URL` is configured later.

## Application rules

- Student accounts are pre-created for PRNs `23021351242001` through `23021351242538` (538 students).
- Students sign in using only PRN and password. The default password is `123456`.
- On first login, students must create a personal password before accessing feedback.
- Feedback has validated 1–5 ratings and is never exposed through edit/delete routes.
- Administrators can add teachers and subjects, view all submissions, and inspect teacher/rating analytics.
- Passwords are stored as Werkzeug hashes, never plaintext.
