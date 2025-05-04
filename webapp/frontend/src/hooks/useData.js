import { API_URL, WS_URL } from '../constants';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Swal from 'sweetalert2'

export function useData({ node, startTime, endTime, numberOfNodes, setNumberOfNodes }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true);

    // Convert from dayjs to timestamp
    const params = {
      startTimeStamp: startTime ? startTime.$d.getTime() : null,
      endTimeStamp: endTime ? endTime.$d.getTime() : null
    }

    // Example: /node/1?startTimeStamp=1630000000000&endTimeStamp=1630000000000
    axios
      .get(`${API_URL}/node/${node}`, {
        params,
        headers: {
          "ngrok-skip-browser-warning": "69420"
        }
      })
      .then(res => setData(res.data))
      .catch(() => setError("Error fetching data"))
  }, [node, startTime, endTime]);

  useEffect(() => {
    if (data) {
      setLoading(false);
    }
    console.log({ data });
  }, [data])

  useEffect(() => {
    // Push notification
    // Define a function to show a notification
    const showNotification = (message, fileUrl) => {
      Swal.fire({
        title: 'Alert!',
        text: message,
        imageUrl: fileUrl,
        imageWidth: 400,
        imageHeight: 200,
        imageAlt: 'Custom image',
      });
    }

    // Request permission for notifications
    Notification.requestPermission().then((result) => {
      if (result === 'granted') {
        console.log('Notification permission granted.');
      }
    });

    // Socket
    console.log({ WS_URL })
    const connection = new WebSocket(WS_URL);

    connection.onopen = () => {
      connection.onmessage = (e) => {
        try {
          let socket = null;
          try {
            socket = JSON.parse(e.data);
          } catch (error) {
            console.log("Error parsing JSON", error);
            return;
          }
          const { name, data: newData } = socket;

          switch (name) {
            case 'connected':
              console.log('connected', data);
              break;
            case 'alert':
              {
                const { message, fileUrl } = data;
                new Notification('Alert!', { body: message });
                showNotification(message, fileUrl);
                break;
              }
            case 'data':
              if (endTime) return;
              if (Number(newData.node) === node)
                setData(prevData => [...prevData, newData]);
              else {
                if (Number(newData.node) > numberOfNodes) {
                  setNumberOfNodes(Number(newData.node))
                }
              }
              break;
            default:
              console.log('Unknown event name:', name);
          }

        } catch (error) {
          console.error(error);
        }
      };
    };

    return () => {
      connection.close();
    }

  }, []);

  const processedData = Array.isArray(data) && data.length > 0 ? {
    x: Object.keys(data[0]).filter(key => key === 'timestamp').map(key => ({
      name: key,
      data: data.map(item => item[key])
    }))[0],
    y: Object.keys(data[0]).filter(key => key !== 'timestamp').map(key => ({
      name: key,
      data: data.map(item => item[key])
    }))
  } : null;

  return { data: processedData, loading, error };
}