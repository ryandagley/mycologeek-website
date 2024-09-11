from flask import Flask, render_template
import requests
from weather import get_weather_data, get_api_key, get_weather_history, get_secrets, get_last_10_days_weather

# define the app variable as Flask
# app = Flask(__name__, template_folder="templates")
app = Flask(__name__)


# Routes to the templates
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


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

    # Fetch historical weather data from S3
    s3_access_name = "cred-keys"
    secret = get_secrets(s3_access_name)

    bucket_name = "mycologeek"

    if secret:
        access_key = secret.get('access_key')
        secret_key = secret.get('secret_key')
        
        # Fetch the last 10 days of weather history
        historical_weather = get_last_10_days_weather(bucket_name, access_key, secret_key)
    else:
        historical_weather = None

    # choose background image based on weather description
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

    # Pass the background image and historical weather data to the template
    return render_template('monitor.html', temperature=temperature, city=city_name, background_image=background_image, historical_weather=historical_weather)

@app.route('/pipe/', methods=["GET", "POST"])
def pipe():
    payload = {}
    headers = {}
    url = "https://s3-us-west-2.amazonaws.com/mycologeek.com/sensor_data.json"
    r = requests.get(url, headers=headers, data={})
    r = r.json()
    return {"res": r}


@app.route('/technical.html')
def technical():
    return render_template('technical.html')


if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=8080)
