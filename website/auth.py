from flask import Blueprint, render_template, request, flash, redirect, url_for

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # TODO: authenticate user (check DB)
        if not username or not password:
            flash("Please enter username and password", category="error")
        else:
            flash("Logged in (stub)", category="success")
            return redirect(url_for('views.home'))

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")

        # Basic validations
        if not username or len(username) < 2:
            flash("Username must be greater than 1 character", category="error")
        elif not password1 or len(password1) < 6:
            flash("Password must be at least 6 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:
            # Create new user logic goes here (hash password, save to DB)
            flash("Account created!", category="success")
            return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth.route("/logout")
def logout():
    # TODO: perform logout (session clear)
    flash("You have been logged out", category="info")
    return redirect(url_for('views.home'))