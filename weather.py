import requests
import boto3
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all logs
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

# List weather files from the S3 bucket and fetch the latest 10
def list_weather_files(bucket_name, s3_client):
    try:
        logging.info(f"Listing objects from bucket: {bucket_name}")
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='weather/')
        
        if 'Contents' in response:
            weather_files = response['Contents']
            file_dates = []
            
            # Log each file found
            logging.info(f"Files found in bucket: {[file['Key'] for file in weather_files]}")

            for file in weather_files:
                key = file['Key']
                logging.debug(f"Processing file: {key}")
                
                # Extract the date part from the filename
                date_str = key.split('/')[-1].split('-weather.json')[0]
                try:
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')
                    file_dates.append((file_date, key))
                except ValueError:
                    logging.warning(f"Invalid date format in filename: {key}")
                    continue
            
            # Log before sorting
            logging.debug(f"Files before sorting: {file_dates}")
            
            # Sort files by date (most recent first)
            file_dates.sort(reverse=True, key=lambda x: x[0])
            
            # Log after sorting
            logging.debug(f"Files after sorting: {file_dates}")
            
            # Return the 10 most recent weather files
            return [key for _, key in file_dates[:10]]
        else:
            logging.info("No weather files found.")
            return []
    except Exception as e:
        logging.error(f"Error listing weather files: {e}")
        return []

# Fetch weather data from a given file in S3
def get_weather_history(bucket_name, file_name, access_key, secret_key):
    logging.info(f"Attempting to fetch file {file_name} from bucket {bucket_name}")
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        logging.info(f"Successfully fetched file content from {file_name}")
        return json.loads(file_content)
    except Exception as e:
        logging.error(f"Failed to fetch weather data from {file_name}: {e}")
        return None

def get_last_10_days_weather(bucket_name, access_key, secret_key):
    s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    # List the last 10 weather files
    weather_files = list_weather_files(bucket_name, s3_client)
    
    logging.info(f"Weather files found: {weather_files}")
    
    if weather_files:
        weather_data = []
        for file in weather_files:
            data = get_weather_history(bucket_name, file, access_key, secret_key)
            if data:
                weather_data.append(data)
        return weather_data
    else:
        logging.error("No weather data available.")
        return []

# Fetch sensor data from S3
def get_sensor_data(bucket_name, file_name, access_key, secret_key):
    logging.info(f"Attempting to fetch sensor data from file {file_name} in bucket {bucket_name}")
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        logging.info(f"Successfully fetched sensor data from {file_name}")
        sensor_data = json.loads(file_content)
        
        # Return the last 20 sensor readings
        return sensor_data[-20:]
    except Exception as e:
        logging.error(f"Failed to fetch sensor data from {file_name}: {e}")
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
    if secret:
        access_key = secret.get('access_key')
        secret_key = secret.get('secret_key')
    
    if access_key and secret_key:
        # Call list_weather_files explicitly to verify it's working
        s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        weather_files = list_weather_files(bucket_name, s3_client)
        logging.info(f"Returned weather files: {weather_files}")
        
        historical_weather = get_last_10_days_weather(bucket_name, access_key, secret_key)
        print("Historical Weather (last 10 days): ", historical_weather)
    else:
        logging.error("Failed to retrieve S3 credentials from Secrets Manager.")
