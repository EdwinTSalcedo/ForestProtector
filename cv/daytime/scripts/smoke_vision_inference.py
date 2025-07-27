
import cv2
import numpy as np
from tensorflow.keras.models import load_model

def load_vision_model(model_path):
    """
    Loads a trained 3D CNN model from the given path.

    Args:
        model_path (str): Path to the Keras model (.h5 or .keras).

    Returns:
        keras.Model: Loaded model.
    """
    try:
        model = load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Failed to load model: {e}")
        return None


def preprocess_video(video_path, img_size=(240, 240), max_frames=30):
    """
    Loads and preprocesses a video into grayscale frames suitable for 3D CNN input.

    Args:
        video_path (str): Path to the input video.
        img_size (tuple): Target size for each frame (width, height).
        max_frames (int): Number of frames to extract from the video.

    Returns:
        np.ndarray or None: Preprocessed video data shaped (1, max_frames, H, W, 1) or None if failure.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while frame_count < max_frames and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, img_size)
        frames.append(resized)
        frame_count += 1

    cap.release()

    if not frames:
        print("No frames extracted.")
        return None

    while len(frames) < max_frames:
        frames.append(np.zeros_like(frames[0]))

    video_array = np.array(frames, dtype=np.uint8)
    video_array = np.expand_dims(video_array, axis=-1)
    video_array = np.expand_dims(video_array, axis=0)
    video_array = video_array / 255.0

    return video_array


def predict_smoke_from_video(model, video_array):
    """
    Predicts smoke presence from preprocessed video input.

    Args:
        model (keras.Model): Loaded 3D CNN model.
        video_array (np.ndarray): Preprocessed video input.

    Returns:
        float: Smoke probability score.
    """
    prediction = model.predict(video_array, verbose=0)
    return float(prediction[0][0])


if __name__ == "__main__":
    model = load_vision_model("smoke.keras")
    video_data = preprocess_video("input_video.mp4")

    if model and video_data is not None:
        prob = predict_smoke_from_video(model, video_data)
        if prob > 0.5:
            print(f"Smoke detected with probability {prob:.2f}")
        else:
            print(f"No smoke detected, probability {prob:.2f}")
