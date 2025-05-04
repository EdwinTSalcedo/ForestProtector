const express = require('express');
const Sensor = require('../models/Data');
const router = express.Router();
const { send_message } = require('../utils/whatsapp_client');
const upload = require('../storage');
const { broadcastAlert } = require('../utils/websockets');
const qrcode = require('qrcode');

// GET endpoint to redirect to docs on root
router.get('/', (req, res) => {
  res.redirect('/api-docs');
});

// POST endpoint to send alert messages
router.post('/alert', upload.single('gif'), async (req, res) => {
  try {
    const { phone, message } = req.body;

    broadcastAlert({
      name: 'alert',
      message,
      fileUrl: `http://localhost:3000/uploads/${req.file.filename}`
    });

    send_message(phone, message);
    res.status(201).send({ message: 'Message sent successfully!' });
  } catch (error) {
    res.status(400).send({ message: 'Error sending message', error });
  }
});

// POST endpoint to receive IoT data
router.post('/node/:node', async (req, res) => {
  try {
    const { co2, temperature, humidity, pressure, sound, smoke } = req.body;
    const { node } = req.params;

    await Sensor.create({
      co2,
      temperature,
      humidity,
      pressure,
      sound,
      smoke,
      node,
    });

    // Broadcast the data to the connected clients
    broadcastAlert({
      name: 'data',
      data: {
        co2,
        temperature,
        humidity,
        pressure,
        sound,
        smoke,
        node,
        timestamp: new Date().getTime(),
      }
    });
    res.status(201).send({ message: 'IoT data added successfully!' });
  } catch (error) {
    console.log('Error adding IoT data:', error);
    res.status(400).send({ message: 'Error adding IoT data', error });
  }
});

// GET endpoint to get the number of nodes registered
router.get('/node-count', async (req, res) => {
  console.log('GET /node-count');
  try {
    const nodeCount = await Sensor.distinct('node').then(nodes => nodes.length);
    nodeCount
      ? res.json({ nodeCount })
      : res.json({ nodeCount: 1 });
  } catch (error) {
    console.log('Error retrieving nodes:', error);
    res.status(400).send({ message: 'Error retrieving nodes', error });
  }
});

// GET endpoint to retrieve the IoT data as JSON
router.get('/node/:node', async (req, res) => {
  try {
    // const { time } = req.query ?? '0'; // 0: all time, 1: last month, 2: last week, 3: last 24 hours, 4: last hour
    const { startTimeStamp, endTimeStamp } = req.query; // Example: /node/1?startTimeStamp=1630000000000&endTimeStamp=1630000000000

    if (startTimeStamp && endTimeStamp) { // Send data between two timestamps
      const data = await Sensor.find({
        node: req.params.node,
        timestamp: {
          $gte: parseInt(startTimeStamp),
          $lte: parseInt(endTimeStamp),
        },
      })
        .select('co2 temperature humidity pressure smoke sound node timestamp')
        .sort({ timestamp: -1 })
        .lean();

      return res.json(data);
    }
    else if (startTimeStamp) { // Send data since a timestamp
      const data = await Sensor.find({
        node: req.params.node,
        timestamp: {
          $gte: parseInt(startTimeStamp),
        },
      })
        .select('co2 temperature humidity pressure smoke sound node timestamp')
        .sort({ timestamp: -1 })
        .lean();

      return res.json(data);
    } else { // Send all data
      const data = await Sensor.find({ node: req.params.node })
        .select('co2 temperature humidity pressure smoke sound node timestamp')
        .sort({ timestamp: -1 })
        .lean();

      return res.json(data);
    }
  } catch (error) {
    res.status(400).send({ message: 'Error retrieving IoT data', error });
  }
});

// Route to render view and send image from process.env.WHATSAPP_QR
router.get('/whatsapp-qr', (req, res) => {
  const qrImageData = process.env.WHATSAPP_QR;
  if (qrImageData === 'Client is ready')
    return res.status(200).send('WhatsApp client is ready');

  if (qrImageData) {
    qrcode.toDataURL(qrImageData, function (err, url) {
      if (err) {
        return res.status(500).send('Error generating QR code');
      }
      res.render('index', { url });
    });
  } else {
    res.status(500).send('QR code data not available');
  }
});

module.exports = router;