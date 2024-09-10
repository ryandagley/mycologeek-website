import serial
import time
import json

# Serial connections for each Arduino on Windows (debug setup... my setup setup)
ports = ["COM6", "COM7"]
serial_connections = [serial.Serial(port, 9600, timeout=1) for port in ports]

# Path to the local file where data will be saved
file_path = "sensor_data1.json"  

# Function to write data to a local file
def write_data_to_local_file(data):
    # Open the file in append mode to add new data
    with open(file_path, 'a') as file:
        json.dump(data, file)  # Write data in JSON format
        file.write('\n')       # Add a new line for each new entry

def collect_and_save_data():
    while True:
        sensor_data = {}

        # Collect data from all the connected Arduinos
        for idx, ser in enumerate(serial_connections):
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Sensor {idx}: {line}")
                sensor_data[f'sensor_{idx}'] = line

        # Add a timestamp to the data
        sensor_data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Save the data to the local file
        write_data_to_local_file(sensor_data)
        
        # Sleep for a few seconds before the next read
        time.sleep(10)

if __name__ == "__main__":
    collect_and_save_data()
