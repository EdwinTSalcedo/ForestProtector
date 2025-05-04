import asyncio
from utils.camera import capture_frames
from utils.models import detect_smoke
from config import Config
import aiohttp
from collections import deque

async def smoke_detector(state_machine):
    config = Config()
    while True:
        # Only proceed if the state machine is in the 'Scanning' state
        if state_machine.state == 'Scanning':
            frames = deque(maxlen=30)  # Adjust maxlen as needed
            async for frame in capture_frames():
                frames.append(frame)

            if len(frames) == 30:
                if detect_smoke(frames):
                    print("Smoke detected!")
                    # TODO: Send frames as GIF @Rodri
                    async with aiohttp.ClientSession() as session:
                        alert_data = {
                            "phone": config.phone_number,
                            "message": "Smoke detected",
                        }
                        # Send alert with frames (mock as GIF)
                        async with session.post(f"{config.endpoint_url}/alert/", json=alert_data) as resp:
                            print(f"Alert sent, status: {resp.status}")
        
        # Sleep briefly to prevent unnecessary CPU usage if not scanning
        await asyncio.sleep(1)  # Mock detection interval
