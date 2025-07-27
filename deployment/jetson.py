"""Main script for Jetson Nano:
- Reads environmental data from serial input
- Uses DQN model to decide camera direction
- Moves servo accordingly
- Uses vision model to detect smoke in the captured video
"""

import serial
import time
import Jetson.GPIO as GPIO
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

SERVO_PIN = 33
FREQ = 50


def setup_servo(pin):
    """Initializes GPIO and PWM to control the servo motor."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, FREQ)
    pwm.start(0)
    return pwm


def set_angle(pwm, angle):
    """Sets the servo to a specific angle."""
    duty_cycle = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.02)


def map_value(value, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def move_servo_to_sector_slow(pwm, current_angle, target_angle, step=1):
    """Gradually moves the servo from the current angle to the target angle."""
    if current_angle < target_angle:
        for angle in range(current_angle, target_angle + 1, step):
            set_angle(pwm, angle)
            time.sleep(0.1)
    else:
        for angle in range(current_angle, target_angle - 1, -step):
            set_angle(pwm, angle)
            time.sleep(0.1)


def move_servo_to_sector(pwm, current_angle, sector):
    """
    Converts a logical sector (1-3) into servo angle and moves the servo.

    Args:
        pwm: PWM object for servo control.
        current_angle (int): Current servo angle.
        sector (int): Target sector (1 to 3).

    Returns:
        int: New servo angle.
    """
    gear_angles = {1: 15, 2: 120, 3: 240}
    if sector in gear_angles:
        gear_angle = gear_angles[sector]
        target_angle = map_value(gear_angle, 0, 450, 0, 180)
        move_servo_to_sector_slow(pwm, current_angle, int(target_angle))
        return target_angle
    print("Invalid sector.")
    return current_angle


def cleanup_servo():
    """Cleans up GPIO resources."""
    GPIO.cleanup()


def preprocess_video_from_camera(cap, img_size=(64, 64), max_frames=30):
    """
    Captures and preprocesses video frames for vision model input.

    Args:
        cap: OpenCV video capture object.
        img_size (tuple): Size to resize frames to.
        max_frames (int): Max number of frames to capture.

    Returns:
        np.ndarray: Processed video array with shape (1, frames, H, W, 1).
    """
    frames = []
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, img_size)
        frames.append(resized)
    cap.release()

    while len(frames) < max_frames:
        frames.append(np.zeros_like(frames[0]))

    video_array = np.array(frames, dtype=np.uint8)
    video_array = np.expand_dims(video_array, axis=-1)
    video_array = np.expand_dims(video_array, axis=0)
    video_array = video_array / 255.0
    return video_array


def read_serial_data(serial_port="/dev/ttyUSB0", baudrate=9600):
    """
    Reads and parses a line of data from the serial port.

    Returns:
        np.ndarray or None: Parsed sensor state or None if invalid.
    """
    with serial.Serial(serial_port, baudrate, timeout=2) as ser:
        line = ser.readline().decode("utf-8").strip()
        print("Received serial:", line)
        parts = line.split(",")
        if len(parts) == 9:
            return np.array([float(x) for x in parts], dtype=np.float32).reshape(1, -1)
        print("Invalid data format.")
        return None


def detect_smoke(cap, model):
    """
    Runs the vision model on video input to detect smoke.

    Args:
        cap: OpenCV video capture object.
        model: Loaded vision model.
    """
    video_input = preprocess_video_from_camera(cap)
    prob = model.predict(video_input, verbose=0)[0][0]
    if prob > 0.5:
        print(f"Smoke detected with probability {prob:.2f}")
        # Placeholder: logic to send alert to a web service
    else:
        print(f"No smoke detected, probability {prob:.2f}")


if __name__ == "__main__":
    pwm = setup_servo(SERVO_PIN)
    current_angle = 0

    dqn_model = load_model("dqn_model.h5", custom_objects={'mse': MeanSquaredError()})
    vision_model = load_model("vision_model.h5")

    try:
        while True:
            state = read_serial_data()
            if state is None:
                continue

            action = np.argmax(dqn_model.predict(state, verbose=0)[0])
            sector = action + 1
            print(f"Suggested sector: {sector}")

            current_angle = move_servo_to_sector(pwm, int(current_angle), sector)
            time.sleep(1)

            cap = cv2.VideoCapture(0)
            detect_smoke(cap, vision_model)

            time.sleep(2)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        pwm.stop()
        cleanup_servo()
        print("GPIO resources released.")
