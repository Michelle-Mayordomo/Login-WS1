from flask import Flask, request, send_from_directory, redirect
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "database", "users.db")


# Login page
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "login.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return send_from_directory(BASE_DIR, "login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    print("LOGIN EMAIL:", email)
    print("LOGIN PASSWORD:", password)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    )

    user = cursor.fetchone()
    connection.close()

    print("DATABASE USER:", user)

    if user:
        return send_from_directory(
            os.path.join(BASE_DIR, "dashboards"),
            "userdashboard.html"
        )

    return "Invalid email or password."


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return send_from_directory(BASE_DIR, "register.html")

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    birthday = request.form["birthday"]
    email = request.form["email"]
    password = request.form["password"]

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (first_name, last_name, birthday, email, password)
        VALUES (?, ?, ?, ?, ?)
        """,
        (first_name, last_name, birthday, email, password)
    )

    connection.commit()
    connection.close()

    return redirect("/")


# CSS, images, and other files
@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)