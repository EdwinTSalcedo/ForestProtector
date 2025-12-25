from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import tensorflow as tf


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cv.daytime.scripts.smoke_vision_inference import (  # noqa: E402
    predict_smoke_from_video,
    preprocess_video,
)
from cv.samples.generate_samples import ensure_samples  # noqa: E402


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


def run_demo() -> None:
    samples = ensure_samples(ROOT / "cv" / "samples")
    model_path = ROOT / "cv" / "daytime" / "models" / "demo_smoke_model.keras"
    input_shape = (30, 240, 240, 1)
    model = load_or_create_demo_model(model_path, input_shape)

    for label, video_path in [("Smoke", samples["day_smoke"]), ("Clear", samples["day_clear"])]:
        video_array = preprocess_video(str(video_path))
        if video_array is None:
            print(f"{label}: failed to load video.")
            continue
        prob = predict_smoke_from_video(model, video_array)
        verdict = "smoke detected" if prob > 0.5 else "no smoke detected"
        print(f"{label}: {verdict} (prob={prob:.2f})")


if __name__ == "__main__":
    np.random.seed(42)
    tf.random.set_seed(42)
    run_demo()
