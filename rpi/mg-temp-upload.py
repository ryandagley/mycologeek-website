import serial
import time
import json
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime

# Serial connections for each Arduino
ports = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
serial_connections = [serial.Serial(port, 9600, timeout=1) for port in ports]

# Base path for local files
local_file_base = "mg-sensor-data"

# S3 bucket details
bucket_name = "mycologeek"
s3_folder = "sensors/"

# Create S3 client
s3_client = boto3.client('s3')

# Get the current date in YYYY-MM-DD format
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# Generate the file paths based on the current date
def get_file_paths():
    current_date = get_current_date()
    local_file_path = f"{local_file_base}-{current_date}.json"
    s3_file_path = f"{s3_folder}{current_date}-sensor-data.json"
    return local_file_path, s3_file_path

# Write data to a local file
def write_data_to_local_file(data, local_file_path):
    with open(local_file_path, 'a') as local_file:
        json.dump(data, local_file)
        local_file.write('\n')  # Add a newline for each entry

# Append data to the S3 file
def append_data_to_s3(data, s3_file_path):
    try:
        # Try to read the existing data from the S3 file
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_path)
            s3_data = response['Body'].read().decode('utf-8')
            sensor_data_list = json.loads(s3_data)
        except s3_client.exceptions.NoSuchKey:
            # If the file doesn't exist, start with an empty list
            sensor_data_list = []

        # Append new data
        sensor_data_list.append(data)

        # Write the updated data back to S3
        s3_client.put_object(Bucket=bucket_name, Key=s3_file_path, Body=json.dumps(sensor_data_list))
        print(f"Data successfully appended to S3: {s3_file_path}")

    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"Failed to append data to S3: {e}")

# Convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (float(celsius) * 9/5) + 32

# Collect sensor data and save locally and in S3
def collect_and_save_data():
    sensor_data = {}
    collected_sensors = {}

    while len(collected_sensors) < len(serial_connections):
        # Collect data from all the connected Arduinos
        for idx, ser in enumerate(serial_connections):
            if ser.in_waiting > 0 and idx not in collected_sensors:
                line = ser.readline().decode('utf-8').strip()
                print(f"Sensor {idx}: {line}")

                # Assuming sensor data contains temperature in Celsius, convert to Fahrenheit
                if "temperature" in line.lower():
                    celsius_value = float(line.split()[-1])  # Assuming the temperature is the last value in the line
                    fahrenheit_value = celsius_to_fahrenheit(celsius_value)
                    collected_sensors[f'sensor_{idx}_temperature_F'] = fahrenheit_value
                else:
                    collected_sensors[f'sensor_{idx}'] = line

    if len(collected_sensors) == len(serial_connections):
       collected_sensors['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")

       local_file_path, s3_file_path = get_file_paths()

       write_data_to_local_file(collected_sensors, local_file_path)

       append_data_to_s3(collected_sensors, s3_file_path)

    else:
        print("Incomplete data from sensors. Nothing appended")


if __name__ == "__main__":
    collect_and_save_data()
