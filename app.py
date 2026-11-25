import os
from functools import wraps

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy import func, inspect, text

from config import Config
from models import Admin, Feedback, Student, Subject, Teacher, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


def is_allowed_prn(prn):
    normalized_prn = str(prn).strip()
    if not normalized_prn.isdigit() or len(normalized_prn) != 14:
        return False
    value = int(normalized_prn)
    return app.config["ALLOWED_PRN_START"] <= value <= app.config["ALLOWED_PRN_END"]


def prn_login_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if isinstance(current_user, Student) and current_user.must_change_password:
            return redirect(url_for("change_password"))
        return view(*args, **kwargs)

    return wrapped


@login_manager.user_loader
def load_user(user_id):
    user_type, identifier = user_id.split(":", 1) if ":" in user_id else ("student", user_id)
    model = Admin if user_type == "admin" else Student
    return db.session.get(model, int(identifier))


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not isinstance(current_user, Admin):
            flash("Administrator access is required.", "danger")
            return redirect(url_for("student_dashboard"))
        return view(*args, **kwargs)

    return wrapped


@app.context_processor
def inject_globals():
    return {"app_name": "Feedback Insight"}


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard" if isinstance(current_user, Admin) else "student_dashboard"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    flash("Student accounts are pre-registered. Sign in with your PRN and default password.", "info")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "")
        user = Student.query.filter_by(student_id=student_id).first()
        if is_allowed_prn(student_id) and user and user.check_password(password):
            login_user(user)
            if user.must_change_password:
                return redirect(url_for("change_password"))
            return redirect(url_for("student_dashboard"))
        flash("Invalid PRN or password. Please use an approved PRN.", "danger")
    return render_template("login.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(request.form.get("password", "")):
            login_user(admin)
            return redirect(url_for("admin_dashboard"))
        flash("Invalid administrator credentials.", "danger")
    return render_template("admin_login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard")
@prn_login_required
def student_dashboard():
    if isinstance(current_user, Admin):
        return redirect(url_for("admin_dashboard"))
    feedback = Feedback.query.filter_by(student_id=current_user.id).order_by(Feedback.submitted_at.desc()).all()
    return render_template("student_dashboard.html", feedback=feedback)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if isinstance(current_user, Admin):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")
        if len(password) < 6:
            flash("New password must contain at least 6 characters.", "danger")
        elif password != confirmation:
            flash("Passwords do not match.", "danger")
        else:
            current_user.set_password(password)
            current_user.must_change_password = False
            db.session.commit()
            flash("Password updated successfully.", "success")
            return redirect(url_for("student_dashboard"))
    return render_template("change_password.html")


@app.route("/feedback", methods=["GET", "POST"])
@prn_login_required
def submit_feedback():
    if isinstance(current_user, Admin):
        return redirect(url_for("admin_dashboard"))
    teachers = Teacher.query.order_by(Teacher.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    if request.method == "POST":
        try:
            teacher_id = int(request.form["teacher_id"])
            subject_id = int(request.form["subject_id"])
            ratings = [int(request.form[key]) for key in ("teaching_quality", "communication_skill", "overall_rating")]
        except (KeyError, TypeError, ValueError):
            flash("Please select valid ratings and academic details.", "danger")
            return render_template("feedback.html", teachers=teachers, subjects=subjects)
        if any(value < 1 or value > 5 for value in ratings) or not request.form.get("comments", "").strip():
            flash("Ratings must be between 1 and 5, and comments are required.", "danger")
        elif not db.session.get(Teacher, teacher_id) or not db.session.get(Subject, subject_id):
            flash("Selected teacher or subject does not exist.", "danger")
        else:
            db.session.add(Feedback(
                student_id=current_user.id, teacher_id=teacher_id, subject_id=subject_id,
                teaching_quality=ratings[0], communication_skill=ratings[1],
                overall_rating=ratings[2], comments=request.form["comments"].strip(),
            ))
            db.session.commit()
            flash("Feedback submitted permanently. It cannot be edited or deleted.", "success")
            return redirect(url_for("student_dashboard"))
    return render_template("feedback.html", teachers=teachers, subjects=subjects)


@app.route("/admin")
@admin_required
def admin_dashboard():
    feedback_count = Feedback.query.count()
    average_rating = db.session.query(func.avg(Feedback.overall_rating)).scalar()
    teacher_rows = db.session.query(Teacher.name, func.count(Feedback.id), func.avg(Feedback.overall_rating)).outerjoin(Feedback).group_by(Teacher.id).order_by(Teacher.name).all()
    subject_rows = db.session.query(Subject.name, func.count(Feedback.id), func.avg(Feedback.overall_rating)).outerjoin(Feedback).group_by(Subject.id).order_by(Subject.name).all()
    rating_rows = db.session.query(Feedback.overall_rating, func.count(Feedback.id)).group_by(Feedback.overall_rating).order_by(Feedback.overall_rating).all()
    latest = Feedback.query.order_by(Feedback.submitted_at.desc()).limit(10).all()
    return render_template("admin_dashboard.html", feedback_count=feedback_count, student_count=Student.query.count(),
                           teacher_count=Teacher.query.count(), subject_count=Subject.query.count(),
                           average_rating=round(average_rating or 0, 2), teacher_rows=teacher_rows,
                           subject_rows=subject_rows, rating_rows=rating_rows, latest=latest)


@app.route("/admin/feedback")
@admin_required
def all_feedback():
    return render_template("feedback_list.html", feedback=Feedback.query.order_by(Feedback.submitted_at.desc()).all())


@app.route("/admin/students")
@admin_required
def manage_students():
    return render_template("students_list.html", students=Student.query.order_by(Student.name).all())


@app.route("/admin/manage/<kind>", methods=["GET", "POST"])
@admin_required
def manage(kind):
    types = {"teachers": (Teacher, "Teacher"), "subjects": (Subject, "Subject")}
    if kind not in types:
        return redirect(url_for("admin_dashboard"))
    model, label = types[kind]
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash(f"{label} name is required.", "danger")
        elif kind == "teachers":
            department = request.form.get("department", "").strip()
            if not department:
                flash("Department is required.", "danger")
            elif Teacher.query.filter_by(name=name).first():
                flash("A teacher with that name already exists.", "danger")
            else:
                db.session.add(Teacher(name=name, department=department))
                db.session.commit()
                flash("Teacher added.", "success")
        else:
            code = request.form.get("code", "").strip().upper()
            if not code:
                flash("Subject code is required.", "danger")
            elif Subject.query.filter((Subject.name == name) | (Subject.code == code)).first():
                flash("A subject with that name or code already exists.", "danger")
            else:
                db.session.add(Subject(name=name, code=code))
                db.session.commit()
                flash("Subject added.", "success")
        return redirect(url_for("manage", kind=kind))
    return render_template("manage.html", kind=kind, label=label, records=model.query.order_by(model.name).all())


@app.route("/api/analytics")
@admin_required
def analytics():
    teacher_rows = db.session.query(Teacher.name, func.count(Feedback.id), func.avg(Feedback.overall_rating)).outerjoin(Feedback).group_by(Teacher.id).order_by(Teacher.name).all()
    subject_rows = db.session.query(Subject.name, func.count(Feedback.id), func.avg(Feedback.overall_rating)).outerjoin(Feedback).group_by(Subject.id).order_by(Subject.name).all()
    ratings = db.session.query(Feedback.overall_rating, func.count(Feedback.id)).group_by(Feedback.overall_rating).order_by(Feedback.overall_rating).all()
    return jsonify({
        "teachers": [{"name": name, "count": count, "average": round(average or 0, 2)} for name, count, average in teacher_rows],
        "subjects": [{"name": name, "count": count, "average": round(average or 0, 2)} for name, count, average in subject_rows],
        "ratings": [{"rating": rating, "count": count} for rating, count in ratings],
    })


def init_database():
    with app.app_context():
        db.create_all()
        columns = {column["name"] for column in inspect(db.engine).get_columns("students")}
        if "must_change_password" not in columns:
            db.session.execute(text(
                "ALTER TABLE students ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT 1"
            ))
            db.session.commit()


if __name__ == "__main__":
    init_database()
    app.run(debug=True)
