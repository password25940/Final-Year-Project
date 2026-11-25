CREATE DATABASE IF NOT EXISTS student_feedback;
USE student_feedback;

-- Run these statements as a MySQL administrator, replacing the placeholder
-- password with the same value used in DATABASE_URL in .env:
-- CREATE USER IF NOT EXISTS 'feedback_user'@'localhost' IDENTIFIED BY 'replace-this-password';
-- GRANT ALL PRIVILEGES ON student_feedback.* TO 'feedback_user'@'localhost';
-- FLUSH PRIVILEGES;

-- The Flask application creates the tables through SQLAlchemy on first start.
-- Run `python seed.py` after configuring DATABASE_URL to add the initial admin,
-- teachers, and subjects.
