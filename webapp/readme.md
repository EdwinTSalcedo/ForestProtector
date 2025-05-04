# Forest Protector

## Description

This is a project to detect and report forest fires in real time. The project is separated into 3 parts:

- backend: responsible for receiving the data from the sensors and send notifications to the frontend and WhatsApp.
- frontend: responsible for showing the data in real time and notify the user about the fires.
- microcontrollers:
  - Jetson: responsible for processing the images and send the data to the backend.
  - NodeMCU: responsible for receiving the data from the sensors and send it to the Jetson.
  - Raspberry: responsible for collecting the data from the sensors and send it through LoRa to the NodeMCU.

## Folder Structure

```bash
.
├── backend # Contains the backend code on node.js.
├── frontend # Contains the frontend code on React.
├── microcontrollers 
│   ├── jetson # Contains the python code for the Jetson.
│   ├── nodeMCU # Contains the arduino code for the NodeMCU.
│   └── piPico # Contains the python code for the Raspberry.
└── readme.md
```
