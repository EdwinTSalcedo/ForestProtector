import pandas as pd
import requests
import time
import random

# URL of your Express.js POST endpoint
url = 'http://localhost:3000/node'  # Adjust based on your setup

# Path to the CSV file
csv_file_path = 'data/mock.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

def send_post(url, node_id, data, index):
    uri = f"{url}/{node_id}"
    print(uri)
    
    response = requests.post(uri, json=data)
    print(f"Response for row {index + 1}: {response.status_code} - {response.text}")

def main():
    for index, row in df.iterrows():
        node_id = row['node']
        data = {
            'co2': row['co2'],
            'temperature': row['temperature'],
            'humidity': row['humidity'],
            'pressure': row['pressure'],
            'smoke': row['smoke'],
            'sound': row['sound'],
            'timestamp': row['timestamp']  # Ensure timestamp is in the correct format
        }
        # Add random delay to simulate real-world conditions
        # time.sleep(random.uniform(0.5, 3)) 
        # if index % 50 == 0 and index != 0:
        #     input("Press Enter to continue...")
        input("Press Enter to continue...")
        send_post(url, node_id, data, index)

if __name__ == '__main__':
    print("Starting data upload...")
    main()
    print("Data upload complete.")
