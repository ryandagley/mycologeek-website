import json
import boto3
import requests
from datetime import datetime

def get_weather_data(city_name, api_key):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'imperial'
    }
    
    # if response fails, give error
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
        
def lambda_handler(event, context):
    # get API key from Secrets Manager
    secret_name = "weatherAPIKey"
    city_name = "Tacoma"
    region_name = "us-west-2"
    
    # Init Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)
    secret_value = client.get_secret_value(SecretId=secret_name)
    api_key = json.loads(secret_value['SecretString'])['Default']
    
    # Fetch weather data
    weather_data = get_weather_data(city_name, api_key)
        
    # Prepare data to store
    weather_info = {
        "city": city_name,
        "date": str(datetime.now()),
        "temperature": weather_data['main']['temp'],
        "humidity": weather_data['main']['humidity'],
        "description": weather_data['weather'][0]['description']
    }
    
    # Save data to S3
    s3 = boto3.client('s3')
    bucket_name = "mycologeek"
    file_name = f"weather/{datetime.now().strftime('%Y-%m-%d')}-weather.json"
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(weather_info),
        ContentType="application/json"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Weather data stored successfully!')
    }