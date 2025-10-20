from flask import Blueprint, render_template, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import requests, datetime
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    # Data cuaca
    forecasts = []
    city = ''

    if request.method == "POST":
        city = request.form.get('city')
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city.lower()}&appid=2d1e72652c7e27411c16bba3bcbd0192&units=metric"
        response = requests.get(url)
        data = response.json()

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
                if i >= 3: # ambil hanya 3 hari pertama
                    break
                    
                day_forecast = {
                    'date': date,
                    'temp_min': min(entry['main']['temp_min'] for entry in entries),
                    'temp_max': max(entry['main']['temp_max'] for entry in entries),
                    'humidity' : entries[0]['main']['humidity'],
                    'condition': entries[0]['weather'][0]['main'],
                    'description': entries[0]['weather'][0]['description'],
                    'icon': entries[0]['weather'][0]['icon']
                }
                forecasts.append(day_forecast)

    return render_template("index.html", user=current_user, today=today, weather=forecasts, city=(city.title() if city else ''))