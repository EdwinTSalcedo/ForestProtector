# Forest Protector Backend

## File Structure

```tree
backend/
├── docker-compose.yml         # Docker configuration for PostgreSQL and Adminer
├── server.js                  # Main Express server
├── routes/                    # Folder for Express routes
│   └── index.js               # Route file for handling IoT data and rendering
├── models/                    # Sequelize models for PostgreSQL
│   └── Data.js                # Model defining IoT data structure
├── views/                     # EJS templates for rendering React
│   └── index.ejs              # EJS file rendering the React app with IoT data
├── public/                    # Static files for serving the React app
│   └── main.js                # React app that uses MUI Charts to display IoT data
├── swagger/                   # Swagger documentation files
│   └── swagger.json           # Swagger configuration for API docs
└── node_modules/              # Dependencies (installed by npm)
```