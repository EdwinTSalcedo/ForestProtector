# Camera Control & Smoke Detection System on Jetson Nano

## Overview

This section of the project integrates two deep learning models on a Jetson Nano to enable intelligent wildfire detection and response:

- **Camera Control Model (DQN)**: A reinforcement learning agent that decides where to point a camera based on sensor readings (temperature, humidity, smoke).
- **Smoke Detection Model (CNN/3D CNN)**: A vision model that analyzes live video to determine the presence of smoke.

---

## Project Components

### 🔧 Scripts

- `DRL.py`  
  → Predicts optimal camera direction manually via terminal input using the DQN model.

- `jetson.py`  
  → Main integrated script to run on Jetson Nano. Reads sensor data via serial, controls a servo motor, and triggers smoke detection from a connected camera.

- `smoke_vision_inference.py`  
  → Predicts smoke presence from a video file using the 3D CNN model.

### 📁 Models

- `dqn_model.h5` or `camera_ctrl.h5`  
  → Trained DQN model for sector prediction.

- `vision_model.h5` or `smoke.keras`  
  → Trained smoke detection model.

---

## Setup & Execution

### 1. Install Dependencies
Create a virtual environment (optional) and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run on Jetson Nano
Ensure models are in the working directory, then run:

```bash
python jetson.py
```

### 3. Manual Testing
Use `DRL.py` or `smoke_vision_inference.py` to test each model individually.

---

## Notes

- Ensure correct serial port access for reading sensor data (`/dev/ttyUSB0`).
- For smoke detection, the camera must be accessible via OpenCV.
- Models must be trained separately and placed alongside the scripts.

---
