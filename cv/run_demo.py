from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from cv.daytime.scripts.smoke_vision_inference import (  # noqa: E402
    predict_smoke_from_video,
    preprocess_video,
)
from cv.nighttime.scripts.fire_detector import detect_fire_in_video  # noqa: E402
SUPPORTED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}


def compute_mean_illumination(video_path: Path, max_frames: int = 30) -> float:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return 0.0
    values = []
    frames = 0
    while frames < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        values.append(float(np.mean(gray)))
        frames += 1
    cap.release()
    if not values:
        return 0.0
    return float(np.mean(values))


def build_demo_model(input_shape: tuple[int, int, int, int]) -> tf.keras.Model:
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Lambda(
        lambda t: tf.reduce_mean(t, axis=[1, 2, 3, 4], keepdims=False)
    )(inputs)
    x = tf.keras.layers.Reshape((1,))(x)
    x = tf.keras.layers.Dense(
        1,
        activation="sigmoid",
        kernel_initializer=tf.keras.initializers.Constant(10.0),
        bias_initializer=tf.keras.initializers.Constant(-3.5),
    )(x)
    model = tf.keras.Model(inputs=inputs, outputs=x)
    return model


def load_or_create_demo_model(model_path: Path, input_shape: tuple[int, int, int, int]) -> tf.keras.Model:
    if model_path.exists():
        return tf.keras.models.load_model(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model = build_demo_model(input_shape)
    model.save(model_path)
    return model


def run_smoke_demo(video_path: Path, model: tf.keras.Model) -> None:
    video_array = preprocess_video(str(video_path))
    if video_array is None:
        print(f"{video_path.name}: failed to load video.")
        return
    prob = predict_smoke_from_video(model, video_array)
    verdict = "smoke detected" if prob > 0.5 else "no smoke detected"
    print(f"{video_path.name}: {verdict} (prob={prob:.2f})")


def run_fire_demo(video_path: Path) -> None:
    detected, _ = detect_fire_in_video(
        str(video_path),
        pixel_threshold=180,
        max_frames=240,
    )
    verdict = "fire detected" if detected else "no fire detected"
    print(f"{video_path.name}: {verdict}")


def collect_sample_videos(samples_root: Path) -> list[Path]:
    videos = [
        path
        for path in samples_root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(videos)


def run_demo(illumination_threshold: float = 87.0) -> None:
    samples_root = ROOT / "cv" / "samples"
    samples = collect_sample_videos(samples_root)
    if not samples:
        print(f"No sample videos found in {samples_root}.")
        print("Add videos to cv/samples and rerun.")
        return
    real_model_path = ROOT / "cv" / "daytime" / "model" / "smoke.keras"
    demo_model_path = ROOT / "cv" / "daytime" / "models" / "demo_smoke_model.keras"
    input_shape = (30, 240, 240, 1)
    if real_model_path.exists():
        model = tf.keras.models.load_model(real_model_path)
    else:
        model = load_or_create_demo_model(demo_model_path, input_shape)

    for video_path in samples:
        mean_luma = compute_mean_illumination(video_path)
        if mean_luma >= illumination_threshold:
            run_smoke_demo(video_path, model)
        else:
            run_fire_demo(video_path)


if __name__ == "__main__":
    np.random.seed(42)
    tf.random.set_seed(42)
    run_demo()
