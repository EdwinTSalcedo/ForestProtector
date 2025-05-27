import os
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def detect_bright_regions(frame, threshold=180):
    """
    Detecta regiones brillantes en un fotograma usando el canal Y (luminancia).
    """
    yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    Y = yuv_frame[:, :, 0]
    decision = np.where(Y > threshold, 1 - (255 - Y) / 128, -1)
    bright_regions = np.where(decision > 0, 255, 0).astype(np.uint8)
    return bright_regions


def calculate_amdf(signal):
    """
    Calcula la función de diferencia de magnitud promedio (AMDF).
    """
    amdf = np.zeros(len(signal) - 1)
    for lag in range(1, len(signal)):
        amdf[lag - 1] = np.mean(np.abs(signal[lag:] - signal[:-lag]))
    return amdf


def detect_periodicity(mean_values, threshold_amdf=0.3):
    """
    Detecta periodicidad en los valores medios usando AMDF.
    """
    amdf = calculate_amdf(mean_values)
    return np.any(amdf < threshold_amdf)


def is_fire_color(frame, mask):
    """
    Verifica si las regiones detectadas tienen colores típicos del fuego.
    """
    fire_region = cv2.bitwise_and(frame, frame, mask=mask)
    hsv_fire_region = cv2.cvtColor(fire_region, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    mask_red = cv2.inRange(hsv_fire_region, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv_fire_region, lower_yellow, upper_yellow)

    fire_color_detected = np.sum(mask_red) + np.sum(mask_yellow) > 0
    return fire_color_detected


def detect_fire_in_video(video_path, pixel_threshold=180, max_frames=300):
    """
    Detecta fuego en un video basado en brillo, periodicidad, color y movimiento.
    """
    cap = cv2.VideoCapture(video_path)
    fire_detected = False
    frame_count = 0
    mean_values = []
    fire_mask = None
    back_sub = cv2.createBackgroundSubtractorKNN()

    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return False, None

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        resized_frame = cv2.resize(frame, (640, 380))
        bright_regions = detect_bright_regions(resized_frame, pixel_threshold)

        if np.any(bright_regions == 255):
            mean_intensity = np.mean(resized_frame[bright_regions == 255])
        else:
            mean_intensity = 0
        mean_values.append(mean_intensity)

        if len(mean_values) >= 200:
            periodicity_detected = detect_periodicity(
                np.array(mean_values[-200:]),
                threshold_amdf=0.5
            )

            if periodicity_detected:
                fire_mask = bright_regions.astype(np.uint8)
                fire_color_detected = is_fire_color(resized_frame, fire_mask)

                fg_mask = back_sub.apply(resized_frame)
                moving_pixels = cv2.countNonZero(fg_mask)

                if fire_color_detected and moving_pixels > 300:
                    fire_detected = True
                    break

    cap.release()
    return fire_detected, fire_mask


def process_single_video(video_path, pixel_threshold=180, max_frames=300):
    """
    Procesa un solo video para verificar la presencia de fuego.
    """
    fire_detected, fire_mask = detect_fire_in_video(
        video_path,
        pixel_threshold,
        max_frames
    )

    if fire_detected:
        print("Fuego detectado en el video.")
    else:
        print("No se detectó fuego en el video.")

    return fire_mask


def main():
    """
    Solicita al usuario la ruta del video y procesa la detección.
    """
    video_path = input("Introduce la ruta del video: ").strip()

    if not os.path.isfile(video_path):
        print("Ruta no válida o archivo no encontrado.")
    else:
        process_single_video(video_path, max_frames=300)


if __name__ == "__main__":
    main()
