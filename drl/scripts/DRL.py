
import tensorflow as tf
import numpy as np

def input_state():
    """
    Reads manual input from the user for temperature, humidity, and smoke level
    for three different sectors.

    Returns:
        np.ndarray: A 1x9 array with all input values formatted for the model.
    """
    print("Enter values for each sector:")
    state = []
    for i in range(1, 4):
        print(f"\nSector {i}:")
        temperature = int(input("  Temperature (0: Below threshold, 1: Above threshold): "))
        humidity = int(input("  Humidity (0: Below threshold, 1: Above threshold): "))
        smoke = float(input("  Smoke level (0–100): "))
        state.extend([temperature, humidity, smoke])
    return np.array(state, dtype=np.float32).reshape(1, -1)

def main():
    """
    Main loop for loading the model, taking user input, making predictions,
    and printing the suggested sector.
    """
    try:
        model = tf.keras.models.load_model('../model/camera_ctrl.h5', compile=False)
        print("Model loaded successfully.\n")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    while True:
        # Get state from user input
        state = input_state()

        # Make prediction
        prediction = model.predict(state, verbose=0)
        print("\nModel prediction:", prediction)

        # Determine suggested sector
        suggested_sector = np.argmax(prediction[0]) + 1
        print(f"\nSuggested sector to attend: Sector {suggested_sector}")

        # Ask if the user wants to continue
        continue_input = input("\nDo you want to make another prediction? (y/n): ").strip().lower()
        if continue_input != 'y':
            break

    print("\nProgram ended.")

if __name__ == "__main__":
    main()