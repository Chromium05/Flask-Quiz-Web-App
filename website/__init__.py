from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
    app.config['SECRET_KEY'] = 'lamkldmsklmaksdm'
    db.init_app(app)

    from .views import views as views_bp
    from .auth import auth as auth_bp

    app.register_blueprint(views_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app

def create_database(app):
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
    print(f"Checking database path: {db_path}")
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('Database Created!')