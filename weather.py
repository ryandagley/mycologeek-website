import requests
import boto3
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Fetch API Key from AWS Secrets Manager
def get_api_key(secret_name, region_name="us-west-2"):
    logging.info(f"Fetching API key from Secrets Manager with secret name: {secret_name}")
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        secret_dict = json.loads(secret)
        return secret_dict["Default"]
    except Exception as e:
        logging.error(f"Error retrieving secret: {e}")
        return None

# Fetch current weather data using OpenWeather API
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
            # Here I fixed the dictionary key where you tried to access a timestamp incorrectly
            weather_info = {
                "temperature": data['main']['temp'],
                "main": data['weather'][0]['main'],
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
        else:
            logging.error(f"Failed to fetch weather data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"API call failed: {e}")
        return None
    
# Fetch Secrets from AWS Secrets Manager
def get_secrets(secret_name, region_name="us-west-2"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        secret_dict = json.loads(secret)
        return secret_dict
    except Exception as e:
        logging.error(f"Error retrieving secret: {e}")
        return None

# Fetch historical weather data from S3
def get_weather_history(bucket_name, file_name, access_key, secret_key):
    logging.info(f"Attempting to fetch file {file_name} from bucket {bucket_name}")
    s3 = boto3.resource('s3',
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)
    try:
        content_object = s3.Object(bucket_name, file_name)
        logging.info(f"Fetching object from S3: {content_object}")
        file_content = content_object.get()['Body'].read().decode('utf-8')
        logging.info("Successfully read file from S3")
        json_content = json.loads(file_content)
        logging.info(f"Parsed JSON: {json_content}")
        logging.info(f"Successfully fetched weather history: {json_content}")
        return json_content
    except Exception as e:
        logging.error(f"Failed to fetch historical weather data from S3: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    secret_name = "weatherAPIKey"
    api_key = get_api_key(secret_name)

    s3_access_name = "cred-keys"
    secret = get_secrets(s3_access_name)
    
    city_name = "Tacoma"
    current_weather = get_weather_data(city_name, api_key)
    print("Current Weather: ", current_weather)
    
    # Access historical weather data from S3
    bucket_name = "mycologeek"
    file_name = "/weather/2024-09-07-weather.json"
    if secret:
        access_key = secret.get('access_key')
        secret_key = secret.get('secret_key')
    
    if access_key and secret_key:
        historical_weather = get_weather_history(bucket_name, file_name, access_key, secret_key)
        print("Historical Weather: ", historical_weather)
    else:
        logging.error("Failed to retrieve S3 credentials from Secrets Manager.")
