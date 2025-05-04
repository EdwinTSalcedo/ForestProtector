import cv2
import imageio
import requests

def main(camera, api_url, json):
    
    cap = cv2.VideoCapture(camera)
    frames = []
    save_frames = False
    frame_number = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Webcam', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'): # Waht triggers the saving of frames
            print("Saving frames...")
            save_frames = True
            
        if save_frames:
            if frame_number % 2 == 0:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frame_number += 1
            if len(frames) == 60:
                save_frames = False
                save_gif(frames, 'captured_frames.gif')
                response = send_gif(
                    'captured_frames.gif', 
                    api_url,
                    json
                )
                print(f'Status Code: {response.status_code}')
                print(f'Response: {response.text}')
                frames = []
                frame_number = 0
        
        if key == ord('q'):
            break
            

    cap.release()
    cv2.destroyAllWindows()
    return frames

def save_gif(frames, filename):
    imageio.mimsave(filename, frames, format='GIF', duration=0.1)

def send_gif(filename, url, json):
    with open(filename, 'rb') as file:
        files = {'gif': file}
        try:
            response = requests.post(url, files=files, data=json)
        except Exception as e:
            print('Error sending GIF:', e)
    return response

if __name__ == "__main__":
    camera = "http://192.168.0.13:5000/video_feed"
    api_url = 'http://localhost:3000/alert'
    json = {
        "phone": "59169761943",
        "message": "Alerta de incendio en el nodo ..."
    }
    
    main(
        camera=camera,
        api_url=api_url,
        json=json
    )