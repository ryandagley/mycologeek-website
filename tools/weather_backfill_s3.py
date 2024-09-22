# This is a script for a one-time run to backfill DynamoDB from S3.

import boto3
import json
from decimal import Decimal
from datetime import datetime

# Initialize S3 and DynamoDB clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Update the region if necessary

# Set your S3 bucket and DynamoDB table names
bucket_name = 'mycologeek'  
table_name = 'WeatherData'

# Get the list of files from the specific S3 folder
def get_weather_files_from_s3():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='weather/')
    files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.json')]
    return files

# Read the file content from S3 and parse the JSON
def read_json_from_s3(file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content, parse_float=Decimal)  # Use Decimal for numeric values to be DynamoDB-compatible

# Write a single record to the DynamoDB table
def write_to_dynamodb(data):
    table = dynamodb.Table(table_name)
    
    # Add a timestamp for when the record is inserted into DynamoDB
    timestamp = str(datetime.utcnow())  # Use UTC timestamp
    
    table.put_item(
        Item={
            'city': data['city'],
            'date': data['date'],  # Original date from the weather file
            'temperature': Decimal(str(data['temperature'])),
            'humidity': Decimal(str(data['humidity'])),
            'description': data['description'],
            'timestamp': timestamp  # The new timestamp when the record is added
        }
    )

# Main function to read from S3 and write to DynamoDB
def main():
    # Get the list of weather files
    files = get_weather_files_from_s3()

    # Iterate over each file and process it
    for file_key in files:
        print(f"Processing file: {file_key}")
        # Read the content of the file
        weather_data = read_json_from_s3(file_key)

        # Write the weather data to DynamoDB
        write_to_dynamodb(weather_data)
        print(f"Successfully written data from {file_key} to DynamoDB.")

if __name__ == '__main__':
    main()
