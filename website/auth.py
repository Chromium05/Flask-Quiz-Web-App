from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return "<h1>Login Page</h1> <br> <a href={{ url_for('auth.register') }}>Go to Signup</a>"

@auth.route("/register")
def register():
    return "<h1>Signup Page</h1> <br> <a href={{ url_for('auth.login') }}>Go to Login</a>"

@auth.route("/logout")
def logout():
    return "<h1>Logout Page</h1>"