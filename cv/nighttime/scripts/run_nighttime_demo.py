from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cv.nighttime.scripts.fire_detector import detect_fire_in_video  # noqa: E402
from cv.samples.generate_samples import ensure_samples  # noqa: E402


def run_demo() -> None:
    samples = ensure_samples(ROOT / "cv" / "samples")
    for label, video_path in [
        ("Fire", samples["night_fire"]),
        ("Clear", samples["night_clear"]),
    ]:
        detected, _ = detect_fire_in_video(
            str(video_path),
            pixel_threshold=180,
            max_frames=240,
        )
        verdict = "fire detected" if detected else "no fire detected"
        print(f"{label}: {verdict}")


if __name__ == "__main__":
    run_demo()
