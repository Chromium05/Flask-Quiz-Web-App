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
    inject_questions(app)

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

def inject_questions(app):
    from .models import Quiz
    with app.app_context():
        questions = [
            Quiz(
                question="What is Python?",
                option_a="A type of snake",
                option_b="A programming language",
                option_c="A kind of coffee",
                option_d="A musical instrument",
                correct_option="B"
            ),
            Quiz(
                question="What does NLP stand for in Artificial Intelligence?",
                option_a="Neural Language Program",
                option_b="Natural Learning Process",
                option_c="Natural Language Processing",
                option_d="Network Logic Protocol",
                correct_option="C"
            ),
            Quiz(
                question="Which of the following is a common task in NLP?",
                option_a="Image recognition",
                option_b="Speech-to-text conversion",
                option_c="Network routing",
                option_d="Data encryption",
                correct_option="B"
            ),
            Quiz(
                question="What is the purpose of tokenization in NLP?",
                option_a="To split text into smaller units such as words or sentences",
                option_b="To encrypt text for security",
                option_c="To remove stop words from data",
                option_d="To correct grammar in sentences",
                correct_option="A"
            ),
            Quiz(
                question="Which library is widely used for NLP tasks in Python?",
                option_a="NumPy",
                option_b="Matplotlib",
                option_c="NLTK",
                option_d="TensorFlow Graphics",
                correct_option="C"
            ),
            Quiz(
                question="What is 'stemming' in NLP?",
                option_a="The process of converting text to lowercase",
                option_b="The process of reducing words to their root form",
                option_c="The process of counting word frequencies",
                option_d="The process of translating text into another language",
                correct_option="B"
            ),
            Quiz(
                question="Which NLP model is known for using the Transformer architecture?",
                option_a="BERT",
                option_b="Naive Bayes",
                option_c="K-Means",
                option_d="Random Forest",
                correct_option="A"
            ),
            Quiz(
                question="What is a 'corpus' in NLP?",
                option_a="A linguistic theory",
                option_b="A collection of text data used for analysis",
                option_c="A language translation model",
                option_d="A machine learning algorithm",
                correct_option="B"
            ),
            Quiz(
                question="In NLP, what are 'stop words'?",
                option_a="Words that end sentences",
                option_b="Words that are ignored during text processing because they add little meaning",
                option_c="Words with negative sentiment",
                option_d="Misspelled words in a dataset",
                correct_option="B"
            ),
            Quiz(
                question="Which NLP task involves identifying whether text expresses a positive, negative, or neutral opinion?",
                option_a="Topic modeling",
                option_b="Sentiment analysis",
                option_c="Part-of-speech tagging",
                option_d="Speech recognition",
                correct_option="B"
            ),
            Quiz(
                question="What is the main goal of Named Entity Recognition (NER) in NLP?",
                option_a="To translate text between languages",
                option_b="To identify and classify entities like names, dates, and locations in text",
                option_c="To summarize large documents",
                option_d="To generate random sentences",
                correct_option="B"
            )
        ]

        db.session.add_all(questions)
        db.session.commit()
        print("Semua pertanyaan sudah ditambahkan ke database")