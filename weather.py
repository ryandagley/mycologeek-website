import requests
import boto3
import json


def get_api_key(secret_name, region_name="us-west-2"):
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        # Retrieve the secret
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        secret_dict = json.loads(secret)
        return secret_dict["Default"]  
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None


def get_current_temperature(city_name, api_key):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'imperial'  # 'imperial' or 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return None