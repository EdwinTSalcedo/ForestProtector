import pandas as pd
import aiohttp
import asyncio

# URL of your Express.js POST endpoint
url = 'http://localhost:3000'  # Adjust based on your setup

# Path to the CSV file
csv_file_path = 'data/mock.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

async def send_post(session, url, node_id, data, index):
    uri = f"{url}/{node_id}"
    print(uri)
    
    async with session.post(uri, json=data) as response:
        print(f"Response for row {index + 1}: {response.status} - {await response.text()}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
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
            tasks.append(send_post(session, url, node_id, data, index))
        await asyncio.gather(*tasks)

print("Starting data upload...")
asyncio.run(main())
print("Data upload complete.")
