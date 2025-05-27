# Fire Detection in Nighttime Video 

This section of the project aims to detect fire in nighttime videos using computer vision techniques by analyzing the brightness, color, periodicity, and movement of suspicious regions. The method is based on the algorithm proposed by Günay et al. [1]. We experimentally tuned the parameters using a video dataset containing forest fire footage that we collected from social media.

### Requirements

Install the dependencies with:

```bash
pip install -r requirements.txt
```

### How to Use

1. Clone the repository or download the files.
2. Make sure you have Python 3.7 or higher installed.
3. Install the dependencies as indicated above.
4. Run the main script with: `python detect_fire.py`

5. When prompted, enter the path of the video you want to analyze:

    Enter the path of the video to analyze: /path/to/video.mp4

6. The system will tell you whether fire has been detected in the video.

### Code Explanation

- `detect_bright_regions()`: identifies bright regions in the video.
- `calculate_amdf()`: calculates signal differences to check for flickering (like that of fire).
- `detect_periodicity()`: checks for periodicity in the intensity of bright regions.
- `is_fire_color()`: analyzes whether the bright regions have typical fire colors (red, yellow).
- `detect_fire_in_video()`: combines all the above functions and determines if fire is present.
- `process_single_video()`: handles user video input and displays the result.

This system can be used to monitor forests, fields, or fire-sensitive facilities during the night.

### References 

[1] O. Günay, K. Taşdemir, B. U. Töreyin, and A. E. Çetin, "Video based wildfire detection at night," *Fire Safety Journal*, vol. 44, no. 6, pp. 860–868, Aug. 2009.
