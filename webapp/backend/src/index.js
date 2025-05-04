const express = require('express');
const connectDB = require('./db'); // Import DB connection
const routes = require('./routes'); // Import routes
const bodyParser = require('body-parser');
const config = require('./config'); // Import config
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./docs/swagger.json');
const cors = require('cors'); // Import the cors module
const http = require('http'); // Import the http module
const { whatsappClient } = require('./utils/whatsapp_client');
const { initWebSocketServer } = require('./utils/websockets'); // Import WebSocket module
const path = require('path');

// Initialize Express
const app = express();
app.use(bodyParser.json());

// Serve static files
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Server PORT
const PORT = config.port || 3000;

// Create HTTP server for WebSockets and Express
const server = http.createServer(app);

// Initialize the WebSocket server
initWebSocketServer(server);

// Connect to MongoDB
connectDB();

// Configures the EJS view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Enable CORS
app.use(cors());

// Parse incoming requests data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Initialize the WhatsApp client
whatsappClient.initialize();

// Register routes
app.use('/', routes);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Start the server (use `server.listen` instead of `app.listen`)
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

module.exports = app;
