// File upload dependencies
const multer = require('multer');
const path = require('path');

// Set up multer for file storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/'); // Specify the destination folder
  },
  filename: function (req, file, cb) {
    cb(null, `${Date.now()}-${file.originalname}`); // Define how the file will be named
  }
});

const upload = multer({
  storage: storage,
  fileFilter: function (req, file, cb) {
    const ext = path.extname(file.originalname);
    if (ext !== '.gif') {
      return cb(new Error('Only .gif files are allowed'));
    }
    cb(null, true);
  }
});

module.exports = upload;