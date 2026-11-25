# Student Feedback Analytics System

## Minor Project Report

**Project type:** Web-based academic minor project  
**Technology:** HTML, CSS, JavaScript, Python Flask, SQLAlchemy, SQLite/MySQL, Chart.js  
**Application:** FeedbackInsight

---

## 1. Abstract

Student Feedback Analytics System is a web application that collects structured feedback from students about teachers and subjects. Students can create accounts, sign in, and submit feedback using a 1–5 rating scale with comments. Administrators can securely access a dashboard, manage students, teachers, and subjects, view all submissions, and analyse teacher-wise, subject-wise, and rating-wise results through charts.

The system keeps submitted feedback immutable. Once a response is submitted, it is stored as a permanent record and no student, faculty member, or administrator can edit or delete it through the application. This improves the reliability and trustworthiness of reports.

The project is implemented with Flask and SQLAlchemy. It uses SQLite by default for simple installation and demonstrations, while MySQL remains supported through the `DATABASE_URL` configuration.

## 2. Introduction

Educational institutions need reliable information about teaching quality, communication, and student satisfaction. Manual feedback collection is slow, difficult to analyse, and can result in lost or inconsistent records. This system provides a central digital platform for collecting and analysing student feedback.

The application separates student and administrator responsibilities. Students can only manage their own account and submit feedback. Administrators can view read-only feedback records and manage the academic reference data used by the feedback form.

## 3. Problem Statement

Traditional paper-based or informal feedback systems have the following problems:

- Feedback is difficult to collect at scale.
- Manual analysis takes time and is prone to errors.
- Teacher and subject performance is difficult to compare.
- Feedback records may be lost or altered.
- Students have no convenient self-service submission process.

## 4. Objectives

1. Provide a simple online feedback form for students.
2. Provide secure student and administrator authentication.
3. Store teacher, subject, student, and feedback information systematically.
4. Preserve submitted feedback as an immutable record.
5. Provide dashboard metrics and graphical analytics.
6. Reduce manual work in feedback collection and reporting.
7. Support a simple local installation for academic demonstrations.

## 5. Scope

### Included

- Student registration and login
- Administrator login
- Teacher and subject management
- Student listing for administrators
- Feedback submission with validated ratings
- Read-only feedback history
- Teacher-wise average ratings
- Subject-wise average ratings
- Rating distribution chart
- SQLite default database and MySQL compatibility
- Responsive web interface

### Not included

- Email or SMS notifications
- Multi-institution tenancy
- Student feedback editing after submission
- Automatic sentiment analysis
- Public API access
- Production cloud deployment

## 6. Users and Roles

### Student

- Register with student ID, name, email, and password.
- Sign in with email and password.
- Select a teacher and subject.
- Rate teaching quality, communication skill, and overall performance.
- Add comments.
- View personal submitted feedback history.

### Administrator

- Sign in through the separate admin portal.
- View dashboard statistics.
- View all feedback submissions.
- View registered students.
- Add teachers.
- Add subjects.
- View teacher, subject, and rating analytics.

## 7. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | The system shall provide pre-created student accounts for PRNs `23021351242001` to `23021351242538`. |
| FR-02 | The system shall authenticate registered students. |
| FR-03 | The system shall authenticate administrators separately. |
| FR-04 | The system shall display available teachers and subjects in the feedback form. |
| FR-05 | The system shall validate ratings between 1 and 5. |
| FR-06 | The system shall require comments before accepting feedback. |
| FR-07 | The system shall permanently store accepted feedback. |
| FR-08 | The system shall prevent feedback editing and deletion through application routes. |
| FR-09 | The administrator shall view total feedback, students, teachers, subjects, and average rating. |
| FR-10 | The system shall display teacher-wise, subject-wise, and rating distribution charts. |

## 8. Non-Functional Requirements

- **Usability:** The interface should be understandable to first-time users.
- **Security:** Passwords must be stored as secure hashes, not plaintext.
- **Integrity:** Feedback must remain unchanged after submission.
- **Validation:** Invalid IDs, missing fields, and invalid ratings must be rejected.
- **Maintainability:** The project should use separate models, templates, configuration, and static files.
- **Portability:** The default SQLite setup should run without a separate database server.
- **Performance:** Dashboard queries should return promptly for a small or medium academic dataset.

## 9. System Architecture

The system follows a layered web architecture:

1. **Presentation layer:** Jinja templates, Bootstrap, custom CSS, and Chart.js.
2. **Application layer:** Flask routes, authentication guards, form validation, and analytics queries.
3. **Data layer:** SQLAlchemy models and SQLite/MySQL database.

### Request flow

```text
Browser
   |
   v
Flask route
   |
   +--> Authentication and validation
   |
   +--> SQLAlchemy model/query
   |
   v
Database
   |
   v
Rendered HTML or JSON analytics
```

## 10. Technology Description

- **HTML5:** Page structure and form controls.
- **CSS3:** Custom visual design, responsive layout, gradients, cards, and tables.
- **Bootstrap 5:** Responsive grid and base components.
- **JavaScript:** Client-side chart initialization and analytics loading.
- **Python:** Backend application logic.
- **Flask:** Routing, sessions, and template rendering.
- **Flask-Login:** User session management and protected routes.
- **SQLAlchemy:** Database abstraction and relationships.
- **SQLite:** Default local database.
- **MySQL/PyMySQL:** Optional production-style database configuration.
- **Chart.js:** Teacher, subject, and rating visualisations.
- **Werkzeug:** Password hashing and verification.

## 11. Database Design

The application uses five main tables.

### Students

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| student_id | String | Unique student identifier |
| name | String | Student name |
| email | String | Unique login email |
| password_hash | String | Secure password hash |
| created_at | DateTime | Registration timestamp |

### Admins

Stores administrator credentials and profile information.

### Teachers

Stores teacher name, department, and creation timestamp.

### Subjects

Stores subject name, unique subject code, and creation timestamp.

### Feedback

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| student_id | Foreign key | Student who submitted |
| teacher_id | Foreign key | Selected teacher |
| subject_id | Foreign key | Selected subject |
| teaching_quality | Integer | Rating from 1 to 5 |
| communication_skill | Integer | Rating from 1 to 5 |
| overall_rating | Integer | Overall rating from 1 to 5 |
| comments | Text | Student comments |
| submitted_at | DateTime | Permanent submission timestamp |

### Relationships

```text
Student 1 -------- * Feedback
Teacher 1 -------- * Feedback
Subject 1 -------- * Feedback
```

Database check constraints ensure all three numeric ratings remain between 1 and 5.

## 12. Module Description

### `app.py`

Contains Flask configuration, authentication, route handlers, access control decorators, feedback validation, management routes, dashboard calculations, and the analytics API.

### `models.py`

Contains SQLAlchemy models for students, administrators, teachers, subjects, and feedback. Password methods use Werkzeug hashing.

### `config.py`

Loads environment variables and selects SQLite by default or another configured SQLAlchemy database URL.

### `seed.py`

Creates database tables and adds the default administrator, sample teachers, and sample subjects.

### Templates

The templates provide landing, authentication, feedback, student dashboard, admin dashboard, management, and read-only report pages.

### Static stylesheet

The custom stylesheet provides the professional visual theme, responsive layout, cards, navigation, tables, forms, and chart containers.

## 13. Main Workflows

### Student workflow

```text
Open application
  -> Create account
  -> Enter an approved PRN
  -> Sign in
  -> Open feedback form
  -> Select teacher and subject
  -> Enter ratings and comments
  -> Submit permanently
  -> View personal history
```

Student login requires an approved PRN and password. The default password is `123456`; the first login requires a personal password update. PRNs outside the configured list are rejected.

### Administrator workflow

```text
Open Admin portal
  -> Sign in
  -> View dashboard metrics
  -> Review charts
  -> View all feedback
  -> Manage students, teachers, and subjects
```

## 14. Security and Data Integrity

- Student and administrator passwords are stored using password hashes.
- Protected routes require an authenticated session.
- Administrator routes use an additional role check.
- Student records are separated from administrator records.
- Foreign keys connect feedback to valid students, teachers, and subjects.
- Rating constraints reject values outside 1–5.
- Feedback has no edit or delete route.
- Duplicate student IDs, emails, teachers, and subject codes are rejected.
- Secret configuration values are stored in `.env`, not in source code.

## 15. Testing

The following tests were completed:

| Test | Result |
|---|---|
| Python syntax compilation | Passed |
| Application landing route | Passed |
| Student registration | Passed |
| Student login | Passed |
| Admin login | Passed |
| Feedback submission | Passed |
| Rating validation | Passed |
| Feedback persistence | Passed |
| Immutable feedback design | Passed |
| Admin analytics endpoint | Passed |
| Student management page | Passed |
| Teacher management page | Passed |
| Subject management page | Passed |
| Redesigned UI route smoke test | Passed |

## 16. Installation and Execution

### One-click method

1. Extract the project folder.
2. Double-click `START_PROJECT.bat`.
3. Open `http://127.0.0.1:5000`.

The launcher creates a virtual environment, installs dependencies, prepares the local database, seeds sample data, and starts the server.

### Manual method

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
python app.py
```

### Default administrator

```text
Email: admin@example.com
Password: admin123
```

The default credentials should be changed before real deployment.

## 17. Advantages

- Easy to use for students and administrators.
- Faster than manual feedback collection.
- Centralised and searchable records.
- Visual analytics support decision making.
- Immutable submissions improve trust.
- No MySQL setup is required for demonstration.
- Modular Flask structure supports future changes.

## 18. Limitations

- The current application is designed for a small or medium institution.
- SQLite is not ideal for high-concurrency production workloads.
- There is no email verification or password reset workflow.
- Chart data is aggregated from current database records only.
- The development Flask server should not be used as a production server.

## 19. Future Enhancements

1. Add email verification and password reset.
2. Add CSV and PDF report export.
3. Add semester, academic year, and department filters.
4. Add anonymous feedback mode with controlled auditability.
5. Add sentiment analysis for comments.
6. Add institution-wide role and permission management.
7. Add production deployment using Gunicorn or a Windows service.
8. Add automated database migrations with Flask-Migrate.
9. Add automated unit and integration test suites.
10. Add notification and scheduled report features.

## 20. Conclusion

The Student Feedback Analytics System successfully provides a complete digital workflow for collecting and analysing student feedback. It solves the main problems of manual feedback collection by combining secure authentication, structured forms, immutable records, administrator management, and graphical reporting in one application.

The project is suitable for academic demonstration and can be extended for institutional deployment by adding stronger production security, migration management, export tools, and advanced analytics.

## 21. Viva Questions and Answers

### Why was Flask used?

Flask is lightweight, flexible, easy to understand, and suitable for building a small academic web application with Python.

### Why is SQLAlchemy used?

SQLAlchemy provides models, relationships, validation constraints, and database portability between SQLite and MySQL.

### How are passwords protected?

Passwords are converted into secure hashes using Werkzeug. The original password is never stored.

### Why is feedback immutable?

Immutable records prevent post-submission changes and make analytics more trustworthy.

### How are ratings validated?

The route validates incoming values and database check constraints enforce a range of 1 to 5.

### How does the dashboard calculate average rating?

SQL aggregate functions calculate the average overall rating grouped by teacher and subject.

### Why does the project use SQLite by default?

SQLite makes the project easy to run and share without requiring a separate database server. MySQL remains available through configuration.

### What is Chart.js used for?

Chart.js converts analytics data into teacher performance, subject performance, and rating distribution charts.
