import asyncio
from config import Config
import cv2
# Mock function for capturing frames
async def capture_frames():
    config = Config()
    camera = config.camera
    
    # Open the camera
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        raise RuntimeError("Could not open camera")

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to a format suitable for further processing
            # For example, converting to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Yield the frame
            yield frame_rgb

            # Sleep to maintain the desired frame rate
            await asyncio.sleep(1/15)  # 15 FPS
    finally:
        # When everything done, release the capture
        cap.release()
