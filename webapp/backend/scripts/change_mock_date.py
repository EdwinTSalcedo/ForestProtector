import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from tqdm import tqdm

# Function to update the timestamps in MongoDB
def update_timestamps(mongo_uri, csv_file_path):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client['test']  # Replace with your DB name
    collection = db['sensors']  # Replace with your collection name
    
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Fetch all documents from MongoDB
    all_data = list(collection.find())
    
    # Loop through each document in MongoDB
    for document in tqdm(all_data):
        # Check if there are remaining rows in the DataFrame to map to
        if not df.empty:
            # Get a random row from the DataFrame
            row = df.sample().iloc[0]
            
            # Extract the original timestamp from the CSV
            original_timestamp = pd.to_datetime(row['timestamp'])
            original_time = original_timestamp.time()

            # Get today's date and combine it with the original time
            today = datetime.now().date()
            new_timestamp = datetime.combine(today, original_time)

            # Update the document in MongoDB
            collection.update_one(
                {'_id': document['_id']},  # Filter by document ID
                {'$set': {'timestamp': new_timestamp}}  # Update the timestamp
            )
            print(f"Updated document with ID {document['_id']} with new timestamp: {new_timestamp}")

    print("All timestamps updated successfully.")

# Main function to run the script
if __name__ == "__main__":
    # Input MongoDB URI and CSV file path
    mongo_uri = input("Enter MongoDB URI: ")
    csv_file_path = "./data/mock.csv"  # Adjust based on your setup
    
    # Call the update function
    update_timestamps(mongo_uri, csv_file_path)
