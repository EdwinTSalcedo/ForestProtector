const dotenv = require('dotenv');

// Load environment variables from the .env file
dotenv.config();

module.exports = {
  mongoURI: process.env.MONGO_URI,
  environment: process.env.ENVIRONMENT,
  port: process.env.PORT || 3000
};
