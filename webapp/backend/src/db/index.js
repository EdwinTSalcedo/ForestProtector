// db/index.js
const mongoose = require('mongoose');
const { mongoURI, environment } = require('../config');

// Function to connect to MongoDB
const connectDB = async () => {
  try {
    console.log("Environment:", environment);
    const URI = mongoURI
    mongoose.connect(URI + '?authSource=admin');

    console.log('MongoDB connected successfully');
  } catch (err) {
    console.error('MongoDB connection error:', err.message);
    process.exit(1); // Exit process with failure
  }
};

module.exports = connectDB;
