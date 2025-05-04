// websocket.js
const { WebSocketServer } = require('ws');

let wss;

const initWebSocketServer = (server) => {
  wss = new WebSocketServer({ server });

  wss.on('connection', function connection(ws) {
    console.log('Client connected');

    // Send a welcome message when a client connects
    ws.send(JSON.stringify({
      name: 'connected',
      data: { message: 'Welcome to the WebSocket server!' }
    }));

    ws.on('error', console.error);

    ws.on('message', function message(data) {
      console.log('received from client: %s', data);
    });

    // When the connection is closed
    ws.on('close', () => {
      console.log('Client disconnected');
    });
  });
};

const broadcastAlert = ({name, message = "", fileUrl = "", data = []}) => {
  if (!wss) return;

  switch (name) {
    case 'alert':
      wss.clients.forEach(client => {
        client.send(JSON.stringify({
          name: 'alert',
          data: { message, fileUrl }
        }));
      });
      break;
    case 'data':
      wss.clients.forEach(client => {
        client.send(JSON.stringify({
          name: 'data',
          data
        }));
      });
  }

};

module.exports = { initWebSocketServer, broadcastAlert };
