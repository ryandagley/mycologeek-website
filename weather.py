import requests
import boto3
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG to capture all logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_secrets(secret_name, region_name="us-west-2"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        secret_dict = json.loads(secret)
        return secret_dict
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

# Fetch API Key from AWS Secrets Manager
def get_api_key(secret_name, region_name="us-west-2"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
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
            logging.error(
                f"Failed to fetch weather data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"API call failed: {e}")
        return None

# Fetch weather history from DynamoDB
def get_weather_history_from_dynamodb(city_name, limit=10):
    dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table('WeatherData')
    
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('city').eq(city_name),
            Limit=limit,
            ScanIndexForward=False  # Get the latest data first
        )
        return response['Items']
    except Exception as e:
        logging.error(f"Error fetching weather history from DynamoDB: {e}")
        return []

# Fetch sensor data from S3
def get_sensor_data(bucket_name, file_name, access_key, secret_key):
    s3 = boto3.resource('s3', aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)
    try:
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        sensor_data = json.loads(file_content)

        filtered_sensor_data = []

        for record in sensor_data[-20:]:
            sensor_0_temperature_F = record.get('sensor_0_temperature_F')
            sensor_1_temperature_F = record.get('sensor_1_temperature_F')
            
            # Null handling if neither sensor has data.
            if sensor_0_temperature_F is None and sensor_1_temperature_F is None:
                continue
            if 'sensor_0_temperature_F' in record:
                record['sensor_0_temperature_F'] = "{:.2f}".format(
                    float(record['sensor_0_temperature_F']))
            if 'sensor_1_temperature_F' in record:
                record['sensor_1_temperature_F'] = "{:.2f}".format(
                    float(record['sensor_1_temperature_F']))

            filtered_sensor_data.append(record)

        return filtered_sensor_data

    except Exception as e:
        logging.error(f"Failed to fetch sensor data from file.")
        return None


if __name__ == "__main__":
    # Example usage
    secret_name = "weatherAPIKey"
    api_key = get_api_key(secret_name)

    s3_access_name = "cred-keys"
    secret = get_secrets(s3_access_name)

    city_name = "Tacoma"
    
    # Get current weather data
    current_weather = get_weather_data(city_name, api_key)
    print("Current Weather: ", current_weather)

    # Get weather history from DynamoDB
    weather_history = get_weather_history_from_dynamodb(city_name)
    print("Weather History (last 10 records): ", weather_history)

    # Fetch sensor data from S3
    bucket_name = "mycologeek"
    if secret:
        access_key = secret.get('access_key')
        secret_key = secret.get('secret_key')

    if access_key and secret_key:
        sensor_data = get_sensor_data(bucket_name, 'sensor_data.json', access_key, secret_key)
        print("Sensor Data: ", sensor_data)
    else:
        logging.error("Failed to retrieve S3 credentials from Secrets Manager.")
