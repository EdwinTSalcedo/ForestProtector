from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


RNG = np.random.default_rng(42)


def _write_video(path: Path, frames: list[np.ndarray], fps: int) -> None:
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    for frame in frames:
        writer.write(frame)
    writer.release()


def _daytime_base_frame(size: tuple[int, int]) -> np.ndarray:
    height, width = size
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    sky_color = np.array([140, 120, 90], dtype=np.uint8)  # BGR
    forest_color = np.array([30, 80, 30], dtype=np.uint8)
    frame[: height // 2] = sky_color
    frame[height // 2 :] = forest_color
    noise = RNG.integers(0, 6, size=frame.shape, dtype=np.uint8)
    frame = cv2.add(frame, noise)
    return frame


def _generate_daytime_clear(num_frames: int, size: tuple[int, int]) -> list[np.ndarray]:
    return [_daytime_base_frame(size) for _ in range(num_frames)]


def _generate_daytime_smoke(num_frames: int, size: tuple[int, int]) -> list[np.ndarray]:
    height, width = size
    frames = []
    for i in range(num_frames):
        frame = _daytime_base_frame(size)
        overlay = frame.copy()
        for blob in range(6):
            cx = int(width * (0.2 + 0.12 * blob) + (i * 0.6) % width)
            cy = int(height * 0.7 - i * 0.4 - blob * 8) % height
            radius = 25 + 5 * blob
            color = (190, 190, 190)
            cv2.circle(overlay, (cx, cy), radius, color, -1)
        frame = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)
        frames.append(frame)
    return frames


def _night_base_frame(size: tuple[int, int]) -> np.ndarray:
    height, width = size
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    sky_color = np.array([20, 20, 40], dtype=np.uint8)
    forest_color = np.array([10, 30, 10], dtype=np.uint8)
    frame[: height // 2] = sky_color
    frame[height // 2 :] = forest_color
    return frame


def _generate_night_clear(num_frames: int, size: tuple[int, int]) -> list[np.ndarray]:
    height, width = size
    frames = []
    star_positions = RNG.integers(
        low=(0, 0),
        high=(width, height // 2),
        size=(40, 2),
    )
    for _ in range(num_frames):
        frame = _night_base_frame(size)
        for x, y in star_positions:
            frame[y, x] = (200, 200, 220)
        frames.append(frame)
    return frames


def _generate_night_fire(num_frames: int, size: tuple[int, int]) -> list[np.ndarray]:
    height, width = size
    frames = []
    base_center = (width // 2, int(height * 0.75))
    for i in range(num_frames):
        frame = _night_base_frame(size)
        overlay = frame.copy()
        flicker = 0.6 + 0.4 * np.sin(2 * np.pi * i / 20)
        jitter_x = int(6 * np.sin(2 * np.pi * i / 15))
        jitter_y = int(4 * np.cos(2 * np.pi * i / 18))
        center = (base_center[0] + jitter_x, base_center[1] + jitter_y)
        radius = 28 + int(6 * np.sin(2 * np.pi * i / 12))
        color = (0, int(140 + 60 * flicker), 255)
        cv2.circle(overlay, center, radius, color, -1)
        for _ in range(3):
            spark_offset = (
                int(RNG.integers(-15, 16)),
                int(RNG.integers(-18, 12)),
            )
            spark_center = (center[0] + spark_offset[0], center[1] + spark_offset[1])
            spark_radius = int(RNG.integers(6, 10))
            cv2.circle(overlay, spark_center, spark_radius, color, -1)
        frame = cv2.addWeighted(overlay, 0.8, frame, 0.2, 0)
        frames.append(frame)
    return frames


def ensure_samples(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    samples = {
        "day_smoke": output_dir / "day_smoke.mp4",
        "day_clear": output_dir / "day_clear.mp4",
        "night_fire": output_dir / "night_fire.mp4",
        "night_clear": output_dir / "night_clear.mp4",
    }

    if all(path.exists() for path in samples.values()):
        return samples

    size = (240, 320)
    _write_video(samples["day_clear"], _generate_daytime_clear(60, size), fps=15)
    _write_video(samples["day_smoke"], _generate_daytime_smoke(60, size), fps=15)
    _write_video(samples["night_clear"], _generate_night_clear(240, size), fps=15)
    _write_video(samples["night_fire"], _generate_night_fire(240, size), fps=15)
    return samples


if __name__ == "__main__":
    samples_dir = Path(__file__).resolve().parent
    ensure_samples(samples_dir)
