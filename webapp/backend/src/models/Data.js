// models/Data.js

const mongoose = require('mongoose');

// Define the sensor data schema
const sensorSchema = new mongoose.Schema({
  co2: Number,
  temperature: Number,
  humidity: Number,
  pressure: Number,
  smoke: Boolean,
  sound: Boolean,
  node: Number,
  timestamp: { type: Date, default: Date.now }
});

// Create and export the Sensor model
module.exports = mongoose.model('Sensor', sensorSchema);