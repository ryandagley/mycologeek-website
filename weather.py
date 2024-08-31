import requests
import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)

def get_api_key(secret_name, region_name="us-west-2"):
    logging.info(f"Fetching API key from Secrets Manager with secret name: {secret_name}")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        # Retrieve the secret
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        secret_dict = json.loads(secret)
        return secret_dict["Default"]  
    except Exception as e:
        logging.error(f"Error retrieving secret: {e}")
        return None

def get_weather_data(city_name, api_key):
    logging.info(f"Fetching weather data for {city_name}")
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'imperial'  # 'imperial' for Fahrenheit, 'metric' for Celsius
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity'],
                "pressure": data['main']['pressure'],
                "temp_max": data['main']['temp_max'],
                "temp_min": data['main']['temp_min'],
                "wind_speed": data['wind']['speed'],
                "wind_direction": data['wind']['deg'],
                "cloudiness": data['clouds']['all'],
                "sunrise": data['sys']['sunrise'],
                "sunset": data['sys']['sunset'],
                "description": data['weather'][0]['description']
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        logging.error(f"API call failed: {e}")
        return None
