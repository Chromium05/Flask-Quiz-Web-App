from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
import requests, datetime, random
from . import db
from .models import User, Quiz

views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    
    forecasts = []
    city = ''

    if request.method == "POST":
        city = request.form.get('city')
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city.lower()}&appid=2d1e72652c7e27411c16bba3bcbd0192&units=metric"
        response = requests.get(url)
        data = response.json()

        # error handling
        if data.get("cod") != "200":
            flash("City not found. Please try again.", category="error")
            return render_template("index.html", weather=None)
        else:
            grouped_forecast = {}
            for entry in data['list']:
                date = entry['dt_txt'].split(' ')[0]
                if date not in grouped_forecast:
                    grouped_forecast[date] = []
                grouped_forecast[date].append(entry)
            
            for i, (date, entries) in enumerate(grouped_forecast.items()):
                if i >= 3:
                    break
                    
                day_forecast = {
                    'date': date,
                    'temp_max': max(entry['main']['temp_max'] for entry in entries),
                    'humidity' : entries[0]['main']['humidity'],
                    'condition': entries[0]['weather'][0]['main'],
                    'description': entries[0]['weather'][0]['description'],
                    'wind_speed': entries[0]['wind']['speed'],
                    'icon': entries[0]['weather'][0]['icon']
                }
                forecasts.append(day_forecast)

    return render_template("index.html", user=current_user, today=today, weather=forecasts, city=(city.title() if city else ''))


@views.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    questions = db.session.query(Quiz).all()

    if ('quiz_order' not in session or 
        'is_answered' not in session or 
        'current_question' not in session or 
        'score' not in session or 
        request.args.get('reset') == '1'):
        
        session['quiz_order'] = [q.id for q in questions]
        random.shuffle(session['quiz_order'])
        session['is_answered'] = [False] * len(questions)
        session['current_question'] = 0
        session['score'] = 0
        session.modified = True

    # submit jawaban
    if request.method == "POST":
        selected = request.form.get('answer')
        
        # Pastikan ada pertanyaan yang sedang dijawab
        if session.get('current_question', 0) > 0:
            current_q_index = session['quiz_order'][session['current_question'] - 1]
            current_question = Quiz.query.get(current_q_index)

            if current_question and selected == current_question.correct_option:
                session['score'] = session.get('score', 0) + 1
                current_user.score += 1
                db.session.commit()
            
            # nandain pertanyaan yang udah dijawab
            session['is_answered'][session['current_question'] - 1] = True
            session.modified = True

    # skip pertanyaan yang udah dijawab
    while (session.get('current_question', 0) < len(session.get('quiz_order', [])) and 
           session.get('is_answered', [])[session['current_question']]):
        session['current_question'] += 1
        session.modified = True

    if session.get('current_question', 0) >= len(session.get('quiz_order', [])):
        final_score = session.get('score', 0)
        total_questions = len(session.get('quiz_order', []))
        
        session.pop('quiz_order', None)
        session.pop('current_question', None)
        session.pop('score', None)
        session.pop('is_answered', None)
        session.modified = True
        
        return render_template("quiz_result.html", score=final_score, total=total_questions)

    # ambil pertanyaan saat ini
    question_id = session['quiz_order'][session['current_question']]
    session['current_question'] += 1
    session.modified = True
    
    question = Quiz.query.get(question_id)
    
    if not question:
        flash("Error: Pertanyaan tidak ditemukan!", category="error")
        return redirect(url_for('views.quiz', reset=1))

    return render_template("quiz.html", 
                         question=question,
                         current_question_number=session['current_question'], 
                         total_questions=len(session['quiz_order']))


@views.route("/leaderboard")
@login_required
def leaderboard():
    users = db.session.query(User).order_by(desc(User.score)).all()
    return render_template("leaderboard.html", users=users)