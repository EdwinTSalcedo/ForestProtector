import requests

def main(api_url, json):
    gif_filename = 'captured_frames.gif'
    response = send_gif(gif_filename, api_url, json)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')

def send_gif(filename, url, json):
    with open(filename, 'rb') as file:
        files = {'gif': file}
        try:
            response = requests.post(url, files=files, data=json)
        except Exception as e:
            print('Error sending GIF:', e)
            return None
    return response

if __name__ == "__main__":
    api_url = 'http://localhost:3000/alert'
    json = {
        "phone": "59169761943",
        "message": "Alerta de incendio en el nodo ..."
    }
    
    main(
        api_url=api_url,
        json=json
    )
