import os

from sqlalchemy.exc import OperationalError

from app import app, init_database
from models import Admin, Student, Subject, Teacher, db


try:
    init_database()
    with app.app_context():
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        if not Admin.query.filter_by(email=admin_email).first():
            admin = Admin(name="System Administrator", email=admin_email)
            admin.set_password(os.getenv("ADMIN_PASSWORD", "admin123"))
            db.session.add(admin)
        if Teacher.query.count() == 0:
            db.session.add_all([
                Teacher(name="Dr. Aisha Khan", department="Computer Science"),
                Teacher(name="Prof. Daniel Mathew", department="Information Technology"),
                Teacher(name="Dr. Meera Shah", department="Mathematics"),
            ])
        if Subject.query.count() == 0:
            db.session.add_all([
                Subject(name="Database Management Systems", code="DBMS"),
                Subject(name="Web Technologies", code="WEB"),
                Subject(name="Data Structures", code="DS"),
            ])
        for prn in range(app.config["ALLOWED_PRN_START"], app.config["ALLOWED_PRN_END"] + 1):
            student_prn = str(prn)
            student = Student.query.filter_by(student_id=student_prn).first()
            if student is None:
                student = Student(
                    student_id=student_prn,
                    name=f"Student {student_prn}",
                    email=f"{student_prn}@students.local",
                )
                db.session.add(student)
            student.set_password(app.config["DEFAULT_STUDENT_PASSWORD"])
            student.must_change_password = True
        db.session.commit()
        print(
            "Seed complete. Student PRNs:",
            app.config["ALLOWED_PRN_START"],
            "to",
            app.config["ALLOWED_PRN_END"],
            "| Default password: 123456",
        )
except OperationalError as error:
    raise SystemExit(
        "Database connection failed. Check DATABASE_URL in .env and ensure "
        "the MySQL user has access to the student_feedback database.\n"
        f"Original error: {error.orig}"
    ) from error
