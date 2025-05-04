import os
from dotenv import load_dotenv

class Config:
    camera = 'http://192.168.0.7:5000/video_feed'
    
    def __init__(self):
        load_dotenv()
        self.endpoint_url = os.getenv("ENDPOINT_URL")
        self.phone_number = os.getenv("PHONE_NUMBER")

# You can extend this to include more configurations.
