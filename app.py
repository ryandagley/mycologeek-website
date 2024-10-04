from flask import Flask, render_template, abort
import os
import requests
from weather import get_weather_data, get_api_key, get_weather_history_from_dynamodb, get_secrets, get_sensor_data
from datetime import datetime
import markdown
import pytz


# Define the app variable as Flask
app = Flask(__name__)

# Pacific Time Zone (Tacoma)
pacific_tz = pytz.timezone('US/Pacific')

# Routes to the templates


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/archive.html')
def archive():
    return render_template('archive.html')


@app.route('/about-ryan.html')
def about_ryan():
    return render_template('about-ryan.html')


@app.route('/blog.html')
def blog():
    return render_template('blog.html')


@app.route('/disclaimer.html')
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/faq.html')
def faq():
    return render_template('faq.html')


@app.route('/gallery.html')
def gallery():
    return render_template('gallery.html')


@app.route('/monitor.html')
def monitor():
    city_name = 'Tacoma'
    secret_name = 'weatherAPIKey'
    api_key = get_api_key(secret_name)
    temperature = get_weather_data(city_name, api_key)

    # Fetch historical weather data from DynamoDB
    historical_weather = get_weather_history_from_dynamodb(city_name)

    # Fetch temperature and humidity data for the chart
    dates = [entry['date'] for entry in historical_weather]
    temperatures = [entry['temperature'] for entry in historical_weather]
    humidities = [entry['humidity'] for entry in historical_weather]

    # Fetch sensor data from S3
    s3_access_name = "cred-keys"
    secret = get_secrets(s3_access_name)

    bucket_name = "mycologeek"
    pacific_time = datetime.now(pacific_tz)
    sensor_file_name = f"sensors/{pacific_time.strftime('%Y-%m-%d')}-sensor-data.json"

    if secret:
        access_key = secret.get('access_key')
        secret_key = secret.get('secret_key')
        sensor_data = get_sensor_data(bucket_name, sensor_file_name, access_key, secret_key)
    else:
        sensor_data = None

    weather_condition = temperature['main'].lower()
    if "clear" in weather_condition:
        background_image = '../img/clear_sky.png'
    elif "rainy" in weather_condition:
        background_image = '../img/rainy_day.png'
    elif "thunderstorm" in weather_condition:
        background_image = '../img/rainy_day.png'
    elif "drizzle" in weather_condition:
        background_image = '../img/rainy_day.png'
    elif "snow" in weather_condition:
        background_image = '../img/snow_day.png'
    else:
        background_image = '../img/mushroom_bg.png'

    # Pass the data to the template
    return render_template('monitor.html', temperature=temperature, city=city_name, 
                           background_image=background_image, historical_weather=historical_weather, 
                           sensor_data=sensor_data, dates=dates, temperatures=temperatures, humidities=humidities)


@app.route('/technical.html')
def technical():
    return render_template('technical.html')


@app.route('/articles/<name>')
def article(name):
    # Path to the Markdown file within the static folder
    filepath = os.path.join(app.static_folder, 'articles', f'{name}.md')

    # Check if the file exists
    if not os.path.exists(filepath):
        abort(404)  # If the file does not exist, return a 404 page

    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    return render_template('article.html', content=html_content, title=name)


if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=8080)
