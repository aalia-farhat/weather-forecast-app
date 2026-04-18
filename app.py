from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_info = None

    if request.method == 'POST':
        city = request.form['city']

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        latitude = geo_data['results'][0]['latitude']
        longitude = geo_data['results'][0]['longitude']

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&past_days=2"
            f"&forecast_days=5"
            f"&timezone=auto"
        )

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        formatted_dates = [
            datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%y")
            for date in weather_data['daily']['time']
        ]

        weather_info = {
            'city': city,
            'temperature': weather_data['current']['temperature_2m'],
            'humidity': weather_data['current']['relative_humidity_2m'],
            'wind_speed': weather_data['current']['wind_speed_10m'],
            'dates': formatted_dates,
            'max_temps': weather_data['daily']['temperature_2m_max'],
            'min_temps': weather_data['daily']['temperature_2m_min']
        }

    return render_template('index.html', weather=weather_info)

if __name__ == '__main__':
    app.run(debug=True)