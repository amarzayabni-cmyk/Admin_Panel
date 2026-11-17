import re
import sqlite3
from io import BytesIO
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file, session, url_for
from openpyxl import Workbook

import config

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = app.config["SECRET_KEY"]

DB_PATH = Path(app.config["DATABASE_PATH"])
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-\(\)]{7,20}$")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def is_admin_logged_in():
    return session.get("admin_logged_in") is True


@app.route("/")
def home():
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        errors = []

        if len(first_name) < 2:
            errors.append("Овог хамгийн багадаа 2 тэмдэгттэй байна.")
        if len(last_name) < 2:
            errors.append("Нэр хамгийн багадаа 2 тэмдэгттэй байна.")
        if not PHONE_REGEX.fullmatch(phone):
            errors.append("Утасны дугаар буруу байна. Жишээ: +976 99112233")
        if not EMAIL_REGEX.fullmatch(email):
            errors.append("Имэйл формат буруу байна. Жишээ: name@example.com")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("register.html")

        try:
            with get_db_connection() as connection:
                connection.execute(
                    "INSERT INTO registrations (first_name, last_name, phone, email) VALUES (?, ?, ?, ?)",
                    (first_name, last_name, phone, email),
                )
            flash("Бүртгэл амжилттай хийгдлээ.", "success")
            return redirect(url_for("success"))
        except sqlite3.IntegrityError:
            flash("Энэ имэйл аль хэдийн бүртгэгдсэн байна.", "error")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        entered_password = request.form.get("password", "")
        if entered_password == app.config["ADMIN_PASSWORD"]:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Нууц үг буруу байна.", "error")

    return render_template("admin_login.html")


@app.route("/admin")
def admin_dashboard():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))

    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT id, first_name, last_name, phone, email, created_at FROM registrations ORDER BY created_at DESC"
        ).fetchall()

    return render_template("admin.html", registrations=rows)


@app.route("/admin/logout")
def logout():
    session.pop("admin_logged_in", None)
    flash("Админ сессийг хааж дууслаа.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin/export")
def export_excel():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))

    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT id, first_name, last_name, phone, email, created_at FROM registrations ORDER BY created_at DESC"
        ).fetchall()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Registrations"
    headers = ["ID", "Овог", "Нэр", "Утас", "Имэйл", "Бүртгэгдсэн огноо"]
    sheet.append(headers)

    for row in rows:
        sheet.append([row["id"], row["first_name"], row["last_name"], row["phone"], row["email"], row["created_at"]])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="registrations.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


init_db()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
