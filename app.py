from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy import text

from utils.ocr import extract_text
from utils.medicine_extractor import extract_medicine_details

import os
import base64
from datetime import datetime, timedelta


app = Flask(__name__)

app.config["SECRET_KEY"] = "ai_medicine_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medicine.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:

            return redirect(
                url_for("login")
            )

        return f(*args, **kwargs)

    return decorated_function


# =========================================================
# USER MODEL
# =========================================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================================================
# MEDICINE MODEL
# =========================================================

class Medicine(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    medicine_name = db.Column(
        db.String(100),
        nullable=False
    )

    strength = db.Column(
        db.String(50)
    )

    dosage = db.Column(
        db.String(100)
    )

    frequency = db.Column(
        db.String(100)
    )

    duration = db.Column(
        db.String(100)
    )

    instructions = db.Column(
        db.String(200)
    )

    # True = current medicine
    # False = old medicine

    is_active = db.Column(
        db.Boolean,
        default=True
    )


# =========================================================
# REMINDER MODEL
# =========================================================

class Reminder(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicine.id"),
        nullable=False
    )

    reminder_time = db.Column(
        db.String(10),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )


# =========================================================
# MEDICINE HISTORY MODEL
# =========================================================

class MedicineHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicine.id"),
        nullable=False
    )

    reminder_time = db.Column(
        db.String(10),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    date = db.Column(
        db.String(20),
        nullable=False
    )


# =========================================================
# DATABASE MIGRATION
# =========================================================

def migrate_database():

    inspector = db.inspect(
        db.engine
    )

    tables = inspector.get_table_names()

    if "medicine" not in tables:

        return

    columns = inspector.get_columns(
        "medicine"
    )

    column_names = [
        column["name"]
        for column in columns
    ]

    with db.engine.connect() as connection:

        # Add user_id if missing

        if "user_id" not in column_names:

            connection.execute(
                text(
                    "ALTER TABLE medicine "
                    "ADD COLUMN user_id INTEGER"
                )
            )

            print(
                "Database updated: user_id added."
            )

        # Add is_active if missing

        if "is_active" not in column_names:

            connection.execute(
                text(
                    "ALTER TABLE medicine "
                    "ADD COLUMN is_active BOOLEAN DEFAULT 1"
                )
            )

            print(
                "Database updated: is_active added."
            )

        connection.commit()


# =========================================================
# ASSIGN OLD DATA TO FIRST USER
# =========================================================

def assign_old_medicines():

    first_user = User.query.order_by(
        User.id.asc()
    ).first()

    if not first_user:

        return

    old_medicines = Medicine.query.filter(
        Medicine.user_id.is_(None)
    ).all()

    if old_medicines:

        for medicine in old_medicines:

            medicine.user_id = first_user.id

            if medicine.is_active is None:

                medicine.is_active = True

        db.session.commit()

        print(
            f"{len(old_medicines)} old medicines "
            f"assigned to user: {first_user.name}"
        )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id

            session["user_name"] = user.name

            assign_old_medicines()

            return redirect(
                url_for("dashboard")
            )

        return "Invalid email or password."

    return render_template(
        "login.html"
    )


# =========================================================
# SIGNUP
# =========================================================

@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        age = request.form["age"]

        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return (
                "Email already registered. "
                "Please login."
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(

            name=name,

            email=email,

            age=age,

            password=hashed_password
        )

        db.session.add(
            new_user
        )

        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template(
        "signup.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    current_user_id = session[
        "user_id"
    ]

    user_medicine_ids = db.session.query(
        Medicine.id
    ).filter(
        Medicine.user_id == current_user_id,
        Medicine.is_active == True
    ).subquery()

    total_medicines = Medicine.query.filter_by(
        user_id=current_user_id,
        is_active=True
    ).count()

    total_reminders = Reminder.query.filter(
        Reminder.medicine_id.in_(
            user_medicine_ids
        )
    ).count()

    total_taken = MedicineHistory.query.filter(
        MedicineHistory.medicine_id.in_(
            user_medicine_ids
        ),
        MedicineHistory.status == "Taken"
    ).count()

    total_missed = MedicineHistory.query.filter(
        MedicineHistory.medicine_id.in_(
            user_medicine_ids
        ),
        MedicineHistory.status == "Missed"
    ).count()

    return render_template(

        "dashboard.html",

        total_medicines=total_medicines,

        total_reminders=total_reminders,

        total_taken=total_taken,

        total_missed=total_missed
    )


# =========================================================
# PRESCRIPTION PAGE
# =========================================================

@app.route("/prescription")
@login_required
def prescription():

    return render_template(
        "prescription.html"
    )


# =========================================================
# UPLOAD PRESCRIPTION
# =========================================================

@app.route(
    "/upload-prescription",
    methods=["POST"]
)
@login_required
def upload_prescription():

    current_user_id = session[
        "user_id"
    ]

    upload_folder = "static/uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = None

    try:

        # =================================================
        # CROPPED IMAGE
        # =================================================

        cropped_image = request.form.get(
            "cropped_image"
        )

        if cropped_image:

            if "," in cropped_image:

                cropped_image = (
                    cropped_image.split(
                        ",",
                        1
                    )[1]
                )

            image_data = base64.b64decode(
                cropped_image
            )

            file_path = os.path.join(
                upload_folder,
                "cropped_prescription.png"
            )

            with open(
                file_path,
                "wb"
            ) as image_file:

                image_file.write(
                    image_data
                )

        else:

            # =================================================
            # NORMAL FILE UPLOAD
            # =================================================

            file = request.files.get(
                "prescription"
            )

            if not file or file.filename == "":

                return (
                    "No prescription image uploaded."
                )

            file_path = os.path.join(
                upload_folder,
                file.filename
            )

            file.save(
                file_path
            )

        # =================================================
        # OCR
        # =================================================

        extracted_text = extract_text(
            file_path
        )

        # =================================================
        # MEDICINE EXTRACTION
        # =================================================

        medicines = extract_medicine_details(
            extracted_text
        )

        # =================================================
        # MEDICINE NOT FOUND
        # =================================================

        if not medicines:

            return render_template(

                "prescription_result.html",

                extracted_text=extracted_text,

                medicines=[],

                medicine_not_found=True
            )

        # =================================================
        # DEACTIVATE OLD MEDICINES
        # =================================================

        old_medicines = Medicine.query.filter_by(

            user_id=current_user_id,

            is_active=True

        ).all()

        for old_medicine in old_medicines:

            # Delete old reminders

            old_reminders = Reminder.query.filter_by(

                medicine_id=old_medicine.id

            ).all()

            for old_reminder in old_reminders:

                db.session.delete(
                    old_reminder
                )

            # Mark old medicine inactive

            old_medicine.is_active = False

        db.session.commit()

        # =================================================
        # SAVE NEW MEDICINES
        # =================================================

        for medicine in medicines:

            new_medicine = Medicine(

                user_id=current_user_id,

                is_active=True,

                medicine_name=medicine[
                    "medicine_name"
                ],

                strength=medicine[
                    "strength"
                ],

                dosage=medicine[
                    "dosage"
                ],

                frequency=medicine[
                    "frequency"
                ],

                duration=medicine[
                    "duration"
                ],

                instructions=medicine[
                    "instructions"
                ]
            )

            db.session.add(
                new_medicine
            )

        db.session.commit()

        # =================================================
        # SHOW RESULT
        # =================================================

        return render_template(

            "prescription_result.html",

            extracted_text=extracted_text,

            medicines=medicines,

            medicine_not_found=False
        )

    finally:

        # =================================================
        # DELETE TEMPORARY IMAGE
        # =================================================

        if (
            file_path
            and os.path.exists(file_path)
        ):

            try:

                os.remove(
                    file_path
                )

            except OSError:

                pass


# =========================================================
# MEDICINES
# =========================================================

@app.route("/medicines")
@login_required
def medicines():

    current_user_id = session[
        "user_id"
    ]

    all_medicines = Medicine.query.filter_by(

        user_id=current_user_id,

        is_active=True

    ).all()

    return render_template(

        "medicines.html",

        medicines=all_medicines
    )


# =========================================================
# REMINDER PAGE
# =========================================================

@app.route("/reminder")
@login_required
def reminder():

    current_user_id = session[
        "user_id"
    ]

    all_medicines = Medicine.query.filter_by(

        user_id=current_user_id,

        is_active=True

    ).all()

    medicine_ids = [

        medicine.id

        for medicine in all_medicines
    ]

    if medicine_ids:

        saved_reminders = Reminder.query.filter(

            Reminder.medicine_id.in_(
                medicine_ids
            )

        ).all()

    else:

        saved_reminders = []

    reminders = []

    for reminder_item in saved_reminders:

        medicine = Medicine.query.filter_by(

            id=reminder_item.medicine_id,

            user_id=current_user_id,

            is_active=True

        ).first()

        if medicine:

            reminders.append({

                "id": reminder_item.id,

                "medicine_id": medicine.id,

                "medicine_name":
                    medicine.medicine_name,

                "strength":
                    medicine.strength,

                "instructions":
                    medicine.instructions,

                "reminder_time":
                    reminder_item.reminder_time,

                "status":
                    reminder_item.status
            })

    return render_template(

        "reminder.html",

        medicines=all_medicines,

        reminders=reminders
    )


# =========================================================
# SET REMINDER
# =========================================================

@app.route(
    "/set-reminder",
    methods=["POST"]
)
@login_required
def set_reminder():

    medicine_id = request.form.get(
        "medicine_id"
    )

    reminder_time = request.form.get(
        "reminder_time"
    )

    if not medicine_id or not reminder_time:

        return (
            "Medicine and reminder time "
            "are required."
        )

    current_user_id = session[
        "user_id"
    ]

    medicine = Medicine.query.filter_by(

        id=int(medicine_id),

        user_id=current_user_id,

        is_active=True

    ).first()

    if not medicine:

        return (
            "Unauthorized medicine selection."
        )

    new_reminder = Reminder(

        medicine_id=medicine.id,

        reminder_time=reminder_time,

        status="Active"
    )

    db.session.add(
        new_reminder
    )

    db.session.commit()

    return redirect(
        url_for("reminder")
    )


# =========================================================
# SAVE MEDICINE HISTORY
# =========================================================

@app.route(
    "/save-history",
    methods=["POST"]
)
@login_required
def save_history():

    medicine_id = request.form.get(
        "medicine_id"
    )

    reminder_time = request.form.get(
        "reminder_time"
    )

    status = request.form.get(
        "status"
    )

    if (
        not medicine_id
        or not reminder_time
        or not status
    ):

        return (
            "Missing history information."
        )

    current_user_id = session[
        "user_id"
    ]

    medicine = Medicine.query.filter_by(

        id=int(medicine_id),

        user_id=current_user_id

    ).first()

    if not medicine:

        return (
            "Unauthorized medicine selection."
        )

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    new_history = MedicineHistory(

        medicine_id=medicine.id,

        reminder_time=reminder_time,

        status=status,

        date=current_date
    )

    db.session.add(
        new_history
    )

    db.session.commit()

    return redirect(
        url_for("history")
    )


# =========================================================
# MEDICINE HISTORY
# =========================================================

@app.route("/history")
@login_required
def history():

    current_user_id = session[
        "user_id"
    ]

    # 90-day retention

    retention_date = (
        datetime.now()
        - timedelta(days=90)
    )

    retention_date_string = (
        retention_date.strftime(
            "%Y-%m-%d"
        )
    )

    user_medicines = Medicine.query.filter_by(

        user_id=current_user_id

    ).all()

    user_medicine_ids = [

        medicine.id

        for medicine in user_medicines
    ]

    if user_medicine_ids:

        old_history = MedicineHistory.query.filter(

            MedicineHistory.medicine_id.in_(
                user_medicine_ids
            ),

            MedicineHistory.date
            < retention_date_string

        ).all()

        for record in old_history:

            db.session.delete(
                record
            )

        db.session.commit()

        history_records = MedicineHistory.query.filter(

            MedicineHistory.medicine_id.in_(
                user_medicine_ids
            )

        ).order_by(

            MedicineHistory.id.desc()

        ).all()

    else:

        history_records = []

    history_data = []

    for record in history_records:

        medicine = Medicine.query.filter_by(

            id=record.medicine_id,

            user_id=current_user_id

        ).first()

        if medicine:

            history_data.append({

                "medicine_name":
                    medicine.medicine_name,

                "reminder_time":
                    record.reminder_time,

                "status":
                    record.status,

                "date":
                    record.date
            })

    return render_template(

        "history.html",

        history=history_data
    )


# =========================================================
# CLEAR HISTORY
# =========================================================

@app.route(
    "/clear-history",
    methods=["POST"]
)
@login_required
def clear_history():

    current_user_id = session[
        "user_id"
    ]

    user_medicines = Medicine.query.filter_by(

        user_id=current_user_id

    ).all()

    user_medicine_ids = [

        medicine.id

        for medicine in user_medicines
    ]

    if user_medicine_ids:

        history_records = MedicineHistory.query.filter(

            MedicineHistory.medicine_id.in_(
                user_medicine_ids
            )

        ).all()

        for record in history_records:

            db.session.delete(
                record
            )

        db.session.commit()

    return redirect(
        url_for("history")
    )


# =========================================================
# CREATE / UPDATE DATABASE
# =========================================================

with app.app_context():

    db.create_all()

    migrate_database()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )