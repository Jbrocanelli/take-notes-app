from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology


# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        session.clear()
        return render_template("signup.html")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for errors
        if not email or not password or not confirmation:
            flash("Email/Password/Confirmation cannot be empty!", "danger")
            return redirect("/signup")

        # Check if password matches confirmation
        if password != confirmation:
            flash("Passwords do not match!", "danger")
            return redirect("/signup")

        # Check if email already exists
        existing_email = db.execute("SELECT * FROM users WHERE email = ?", email)
        if existing_email:
            flash("This email is already registered", "danger")
            return redirect("/signup")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Generate new user with singup information
        new_user = db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, hashed_password)

        #log user in
        session["user_id"] = new_user
        flash("Registration successful! You can now log in.", "success")

        return redirect("/login")


@app.route("/login", methods =["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check for errors:
        if not email or not password:
            flash("email and/or password cannot be empty!", "danger")
            return redirect("/login")

        # Check if email and password are valid
        user_db = db.execute("SELECT * FROM users WHERE email = ?", email)
        if len(user_db) != 1 or not check_password_hash(user_db[0]["hash"], password):
            flash("Invalid email and/or password!", "danger")
            return redirect("/login")

        # if there are no erros log user in
        session["user_id"] = user_db[0]["id"]
        flash("Logged in!", "success")

        # Redirect to notes after login in
        return redirect("/")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Get which user has logged in
    user_id = session.get("user_id")

    if request.method == "POST":
        # add a new note
        note_content = request.form.get("note")
        note_date = request.form.get("date")
        note_id = request.form.get("note_id")
        color = request.form.get("color")

        if note_id and color:
             db.execute("UPDATE notes SET color = ? WHERE id = ? AND user_id = ?", color, note_id, user_id)
             flash("Note color updated!", "success")
             return redirect("/")

        if note_content and note_date:
            db.execute("INSERT INTO notes (user_id, notes, date) VALUES (?, ?, ?)", user_id, note_content, note_date)
            flash("Note added!", "success")
            return redirect("/")

        elif note_content:
            db.execute("INSERT INTO notes (user_id, notes) VALUES (?, ?)", user_id, note_content)
            return redirect("/")

        else:
            return redirect("/")


    else:
        # Get user data
        notes = db.execute("SELECT * FROM notes WHERE user_id = ?", user_id)
        return render_template("index.html", notes=notes)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/delete_note/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    user_id = session.get("user_id")

    note = db.execute("SELECT * FROM notes WHERE id = ? AND user_id = ?", note_id, user_id)
    if len(note) != 1:
        return redirect("/")

    db.execute("DELETE FROM notes WHERE id = ?", note_id)
    flash("Note deleted!", "success")
    return redirect("/")


@app.route("/edit_note/<int:note_id>", methods=["POST"])
@login_required
def edit_note(note_id):
    user_id = session.get("user_id")
    new_content = request.form.get("note")
    new_date = request.form.get("date")

    if not new_content:
        flash("Note content cannot be empty", "danger")
        return redirect("/")

    db.execute("UPDATE notes SET notes = ?, date = ? WHERE id = ? AND user_id = ?", new_content, new_date, note_id, user_id)

    flash("Note updated succesfully!", "success")
    return redirect("/")

